setwd('~/Documents/aulas/IBm_day_2025/')

rm(list = ls())
gc()

packages2load <- c('ggplot2', 'dplyr', 'heatmap3', 'pheatmap', 'plotly', 'RColorBrewer')

lapply(packages2load, library, character.only=TRUE)

source('r_functions/functions.R')

clin_f <- readRDS('data/UCEC_Clinical_522.rds')

exprData <- readRDS('data/UCEC_EXPRS_Normalized_filtered.rds')

dd <- dist(exprData, method = 'euclidean')
hhc <- hclust(dd, method = 'ward.D2')
hhc$height <- hhc$height/max(hhc$height)
aCalinski <- calinski(hhc, gMax = 9)

# Calinski-Harabasz calcula a razão entre a variância entre os grupos e a variância dentro do grupo. Uma proporção maior sugere que os clusters são bem separados e compactos, o que significa que os pontos de dados dentro de um cluster estão próximos uns dos outros e distantes de pontos em outros clusters.

jobName = 'TCGA UCEC'
mmain = paste0(jobName, " (", nrow(exprData), " samples/", ncol(exprData), " genes)")

plot(hhc, hang = -1, labels = FALSE, sub = "", main = mmain, xlab = '')
obj <- aCalinski/max(aCalinski) * 0.67
G <- length(obj)
ccol <- rep("black", G)
for (g in 2:(G - 1)) {
  check <- obj[g - 1] < obj[g] & obj[g + 1] < obj[g]
  if (check)
    ccol[g] <- "red"
}
xx <- floor(seq(from = 1, to = length(hhc$labels)*0.75, length.out = G))
nums <- paste(1:G); nums[1] <- ""
obj <- obj + 0.3
text(xx, obj, nums, col = ccol)
lines(xx, obj, col = "gray30", lty = "longdash")


### Plotar um heatmap

heatmap3(t(as.matrix(exprData)), Colv = as.dendrogram(hhc), ColSideColors = clin_f$subtype_cols)

clin_f$Cluster_3 <- cutree(hhc, 3)

table(clin_f$Cluster_3)
clin_f$SUBTYPE <- as.factor(clin_f$SUBTYPE)
table(clin_f$Cluster_3, clin_f$SUBTYPE)

### PCA

pca.ucec <- prcomp(exprData)
plot(pca.ucec$x[,1], pca.ucec$x[,2], col=clin_f$Cluster_3, pch=19)

plot(pca.ucec$x[,1], pca.ucec$x[,2], col=clin_f$subtype_cols, pch=19)
