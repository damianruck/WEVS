library(psych)

setwd('/Users/damianruck/WVS_blog_post')

D <- read.csv(file = "df_vals_for_compression.csv", header = TRUE)

print(dim(D))
#print(head(D))

drops <- c('S017')

#extract the colujnm for ite weights and drop it from the large df
weights <- D['S017']
D <- D[ , !(names(D) %in% drops)]

D[D<0] <- NA # set missing values (negatives) to nas

ww <- c()
for (wi in weights) {
    ww <- c(ww,wi)
}

# print(dim(D))

#print(as.vector(weights))
#print(type(weights))
#print(length(ww))

#weights <- as.vector(weights)


#fit the factor analysis model and extract and save the values of interest
fit <- fa(D, nfactors=7, rotate='oblimin',fm='ml',missing=TRUE)#, weight=ww)

x<-fit$values
load<-fit$loadings
scores<-fit$scores

write.csv(load, 'Ruck_etal/Rucketal_loadings.csv')
write.csv(scores, 'Ruck_etal/Rucketal_variables.csv')