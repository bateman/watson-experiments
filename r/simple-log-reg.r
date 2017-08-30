dataset <- read.csv2('logit-dataset.csv')
dataset = na.omit(dataset)

logit <- glm(formula=Successful ~I(PropensityToTrust=='HIGH'), data=dataset, family=binomial())
res = summary(logit)
capture.output(res, file="regression.txt")
estimate = res$coefficients[2,1]
estimate = round(exp(estimate), 2)
v <- "Odds ratio"
capture.output(v, file="regression.txt", append = TRUE)
capture.output(estimate, file="regression.txt", append = TRUE)

library(pROC)
prob=predict(logit, type="response")
dataset$prob=prob
#creazione della curva
g <- roc(Successful ~ prob, data = dataset)
#visualizzazione della curva
plot(g)

newdata = data.frame(PropensityToTrust='HIGH')
predict.glm(logit, newdata, type="response")
newdata = data.frame(PropensityToTrust='LOW')
predict.glm(logit, newdata,type="response")
