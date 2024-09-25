#De la ligne 1 à 90, code de base avec le modèle
#Les lignes après correspondent au code pour créer une carte, la courbe de dommage et l'afficher sur une page web avec la librairie (shiny)

library(data.table)
library(ggplot2) #facultative, utile pour l'application shiny
library(sf) #facultative, utile pour l'application shiny
library(leaflet) #facultative, utile pour l'application shiny
library(shiny) #facultative, utile pour l'application shiny
library(DT) #facultative, utile pour l'application shiny

# Chemin des fichiers, à changer en fonction du poste
path <- "C:/Users/User/Documents/dev/R/CCR/"
fichier_prtf <- "Portefeuille.csv"
fichier_couredommage <-"CourbeDommages.csv"

#-----------------------------------------------------------------------------------------------------------------------
#Création et application du modèle


portefeuille <- fread(paste0(path, fichier_prtf), encoding = "UTF-8")
courbe_dommages <- read.csv(file.path(path, fichier_couredommage))


# Définir la fonction d'interpolation linéaire avec le dataframe courbe_dommages
interpolate_destruction <- function(hauteur, data) {
  result <- approx(data$HauteurEau_M, data$TauxDestruction, xout = hauteur)
  return(result$y)
}

#test de ma fonction d'interpolation
#taux_destruction_estime <- interpolate_destruction(7.5, courbe_dommages)


#Modèle aléa 
#Les 6 premières lignes sont l'entête avec le nombre de colonnes, de lignes, la taille de cellule, la valeur nodata et les coordonnées de la maille en bas à gauche
alea_ascii <- "HMaxProba_SudEst_274_100.asc"
alea_inondation <- fread(paste0(path, alea_ascii), skip = 6)
alea_matrix <- as.matrix(alea_inondation)

file_path <- paste0(path, alea_ascii)

# Ouvrir le fichier en mode lecture, ce qui va permettre d'extraire les valeurs de l'entête
file_connection <- file(file_path, "r")
lines <- readLines(file_connection) # Lire les lignes du fichier
close(file_connection) # Fermer la connexion au fichier


ncols <- as.numeric(sub("ncols ", "", lines[1]))
nrows <- as.numeric(sub("nrows ", "", lines[2]))
xllcorner <- as.numeric(sub("xllcorner ", "", lines[3]))
yllcorner <- as.numeric(sub("yllcorner ", "", lines[4]))
cellsize <- as.numeric(sub("cellsize ", "", lines[5]))



#Code qui parcourt toutes les longitudes latitudes de portefeuille puis calcule la distance par rapport à la coordonnée en bas à gauche puis on retrouve la hauteur d'eau correspondante
portefeuille$HauteurEau_M <- numeric(nrow(portefeuille)) # Création  d'une colonne vide "HauteurEau_M" pour stocker les valeurs d'hauteur d'eau

# Boucle pour parcourir toutes les lignes de portefeuille
for (i in 1:nrow(portefeuille)) {
  ligne_i_colonnes_X1_Y1 <- portefeuille[i, c("X", "Y")]
  x1_value <- ligne_i_colonnes_X1_Y1$X  # longitude
  y1_value <- ligne_i_colonnes_X1_Y1$Y  # latitude
  
  # Calcul des distances X et Y en Lambert93
  distance_X <- x1_value-xllcorner
  distance_Y <- y1_value-yllcorner
  # Accès à la valeur correspondante dans alea_inondation et stockage dans la colonne créée "HauteurEau_M"
  portefeuille$HauteurEau_M[i] <- alea_matrix[nrows - floor(distance_Y / cellsize), floor(distance_X / cellsize)]
}





#Calcul du cout moyen de destruction avec la fonction d'interpolation pour avoir le taux de destruction correspondant à la hauteur d'eau
portefeuille$TxDestruction <- sapply(portefeuille$HauteurEau_M, interpolate_destruction, courbe_dommages)
portefeuille$MontantDommage <- portefeuille$ValeurAssuree*portefeuille$TxDestruction
#head(portefeuille)

# Calcul de la somme de la colonne MontantDommage et formatage avec des séparateurs pour les milliers
somme_montant_dommage <- format(sum(portefeuille$MontantDommage), big.mark = " ")
cat("Le montant total des dommages est de ", somme_montant_dommage, "€\n")

#library(writexl)
#path_file <- "C:/Users/User/Documents/dev/R/CCR/DommagesPortefeuille.xlsx"
#write_xlsx(portefeuille, path_file)




#-----------------------------------------------------------------------------------------------------------------------
#Création de la carte avec les sites et de la courbe dommages


# Création  d'un objet sf avec les coordonnées X et Y et projection des coordonnées en latitude et longitude (WGS 84)
portefeuille_sf <- st_as_sf(portefeuille, coords = c("X", "Y"), crs = 2154)
portefeuille_sf <- st_transform(portefeuille_sf, crs = 4326)  

# Ajout des colonnes X1 et Y1 avec les coordonnées projetées
portefeuille_sf$X1 <- st_coordinates(portefeuille_sf)[, 1]
portefeuille_sf$Y1 <- st_coordinates(portefeuille_sf)[, 2]


#Visualisation de Portefeuille
# Normaliser la variable ValeurAssuree pour définir des poids entre 0 et 1
min_val <- min(portefeuille$MontantDommage)
max_val <- max(portefeuille$MontantDommage)
portefeuille_sf$Poids <- (portefeuille$MontantDommage - min_val) / (max_val - min_val)

coordinates_prtf <- sf::st_coordinates(portefeuille_sf)


# Définir une taille maximale et minimale pour les cercles
taille_max <- 15  # Taille maximale
taille_min <- 5   # Taille minimale

# Calcul du rayon des cercles en utilisant pmax pour maintenir la taille minimale
portefeuille_sf$Rayon <- pmax(portefeuille_sf$Poids * taille_max, taille_min)

# Ajout d'une colonne de couleurs en fonction de la variable Risque
portefeuille_sf$Couleur <- factor(portefeuille$Risque, levels = c("Appartement", "Maison", "Villa", "Entreprise"),
                                  labels = c("yellow", "blue", "green", "orange"))

# Créer une carte leaflet
map <- leaflet() %>%
  addTiles()  # Ajouter des tuiles de carte de base (OpenStreetMap)

# Ajout des cercles proportionnels en fonction de la variable ValeurAssuree
map <- map %>%
  addCircleMarkers(
    data = portefeuille_sf,
    radius = ~Rayon,
    label = ~paste("ID:", ID, "Risque:", Risque, "Etage:", Etage, "Usage:", Usage, "Valeur Assurée:", ValeurAssuree),
    popup = ~paste("Montant dommages : ", format(round(MontantDommage, 2), big.mark = " "), "€"),
    color = ~Couleur,
    fillOpacity = 0.7
  )

#Ajout de la légende
palette_couleurs <- c("yellow", "blue", "green", "orange")

# légende personnalisée
legend_colors <- palette_couleurs
legend_labels <- c("Appartement", "Maison", "Villa", "Entreprise")

# Ajout de la légende
map <- map %>%
  addLegend(
    position = "bottomright",  
    colors = legend_colors,  
    labels = legend_labels,  
    title = "Légende" 
  )





# Création  d'un objet sf avec les coordonnées Lambert 93
coord_lambert <- st_sfc(st_point(c(xllcorner, yllcorner)), crs = 2154)

# Transformer les coordonnées Lambert 93 en coordonnées géographiques (WGS 84 - EPSG:4326)
coord_geo <- st_transform(coord_lambert, 4326)

#Extraction longitudes et latitudes de coord_geo
longitude_maille1 <- st_coordinates(coord_geo)[, "X"]
latitude_maille1 <- st_coordinates(coord_geo)[, "Y"]

# Ajouter le point coord_geo à la carte
map <- map %>%
  addMarkers(
    data = coord_geo,  
    lng = longitude_maille1,  
    lat = latitude_maille1, 
    label = "Point Maille 1", 
  )

# Afficher la carte
map



# Tracer la courbe de courbe_dommages
ggplot(courbe_dommages, aes(x = HauteurEau_M, y = TauxDestruction)) + geom_line() + labs(title = "Courbe de Dommages", x = "Hauteur d'Eau (m)", y = "Taux de Destruction")


#-----------------------------------------------------------------------------------------------------------------------
#Création de l'application Shiny

# Définition de l'interface utilisateur
ui <- fluidPage(
  
  # En-tête de l'application
  headerPanel("Modélisation simplifiée des dommages en inondation"),
  
  # Sélection du contenu
  sidebarLayout(
    mainPanel(
      tabsetPanel(
        tabPanel(
          "Tableau de Portefeuille", 
          DTOutput("table"),
          class = "mx-auto"
        ),
        tabPanel(
          "Courbe de Dommages", 
          plotOutput("courbe"),
          class = "mx-auto"
        ),
        tabPanel(
          "Carte des localisations du portefeuille et de la maille1 de l'aléa inondations", 
          leafletOutput("map"),
          class = "mx-auto"
        )
      )
    ),
    sidebarPanel(
      # Affichage du montant total des dommages avec "€"
      h3(paste("Montant total des dommages :", somme_montant_dommage, "€")),
    )
  )
)

# Définition du serveur
server <- function(input, output) {
  
  # Affichage du montant total des dommages
  output$montant_total <- renderText({
    somme_montant_dommage
  })
  
  # Affichage du tableau de portefeuille avec MontantDommage
  output$table <- renderDT({
    portefeuille$MontantDommage <- formatC(portefeuille$MontantDommage, format = "f", digits = 2, big.mark = " ", decimal.mark = ",")
    datatable(portefeuille, options = list(pageLength = 10))
  })
  
  # Affichage de la courbe de dommages
  output$courbe <- renderPlot({
    ggplot(courbe_dommages, aes(x = HauteurEau_M, y = TauxDestruction)) + geom_line() + labs(title = "Courbe de Dommages", x = "Hauteur d'Eau (m)",y = "Taux de Destruction")
  })
  
  # Affichage de la carte
  output$map <- renderLeaflet({
    map
  })
}

# Exécution de l'application Shiny
shinyApp(ui, server)













