# lecture de la table
tabicu <- read.csv("C:/Users/imt/Documents/Mes dossiers de travail/ENSEIGNEMENT/M2R Epidémiologie/ML&MLG/TP/ICU.csv", sep=";")
attach(tabicu)
sexe=as.factor(sexe)
chir=as.factor(chir)
inf=as.factor(inf)
tabicu 
names(tabicu)

# Stat univariée sur variables quantitatives
summary(tabicu[,c("age","fc","tas","glasgow")])

# Table de fréquence sur variables qualitatives
eff.dcd=table(dcd)
prop.dcd=prop.table(table(dcd))
rbind(eff.dcd,prop.dcd)

eff.sexe=table(sexe)
prop.sexe=prop.table(table(sexe))
rbind(eff.sexe,prop.sexe)

eff.chir=table(chir)
prop.chir=prop.table(table(chir))
rbind(eff.chir,prop.chir)

eff.inf=table(inf)
prop.inf=prop.table(table(inf))
rbind(eff.inf,prop.inf)

# Tableau croisé avec dcd 
table(dcd,sexe)
prop.table(table(dcd,sexe),2)
chisq.test(dcd, sexe, correct=FALSE)

table(dcd,chir)
prop.table(table(dcd,chir),2)
chisq.test(dcd, chir, correct=FALSE)

table(dcd,inf)
prop.table(table(dcd,inf),2)
chisq.test(dcd, inf, correct=FALSE)

# Analyse de variance selon dcd 
par(mfrow=c(2,2))

boxplot(tas~dcd, ylab="TAS", xlab="Décès")
aov.dcd1 = aov(tas~dcd)
summary(aov.dcd1)
model.tables(aov.dcd1,type="means") 

boxplot(age~dcd, ylab="Age", xlab="Décès")
aov.dcd2 = aov(age~dcd)
summary(aov.dcd2)
model.tables(aov.dcd2,type="means")

boxplot(fc~dcd, ylab="FC", xlab="Décès")
aov.dcd3 = aov(fc~dcd)
summary(aov.dcd3)
model.tables(aov.dcd3,type="means")

boxplot(glasgow~dcd, ylab="Glasgow", xlab="Décès")
aov.dcd4 = aov(glasgow~dcd)
summary(aov.dcd4)
model.tables(aov.dcd4,type="means")

# Regression logistique

#selon une variable explicative qualitative

m1.chir = glm(dcd ~ as.factor(chir), family="binomial")
anova(m1.chir, test="Chisq")
summary(m1.chir)

m1.sexe = glm(dcd ~ sexe, family="binomial")
anova(m1.sexe, test="Chisq")
summary(m1.sexe)

m1.inf = glm(dcd ~ as.factor(consc), family="binomial")
anova(m1.inf, test="Chisq")
summary(m1.inf)
predict(m1.inf,type="response")

#selon une variable explicative quantitative
par(mfrow=c(2,2))

m2.glasgow = glm(dcd ~ glasgow, family="binomial")
summary(m2.glasgow)
anova(m2.glasgow,test="Chisq")
plot(glasgow,dcd,ylab="probabilité prédite de décès")
xp=seq(min(glasgow),max(glasgow))
yp=predict(m2.glasgow,data.frame(glasgow=xp),type="response")
lines(xp,yp,col="red")

m2.age = glm(dcd ~ age, family="binomial")
summary(m2.age)
plot(age,dcd,ylab="probabilité prédite de décès")
xp=seq(min(age),max(age))
yp=predict(m2.age,data.frame(age=xp),type="response")
lines(xp,yp,col="blue")

m2.tas = glm(dcd ~ tas, family="binomial")
summary(m2.tas)
plot(tas,dcd)
xp=seq(min(tas),max(tas))
yp=predict(m2.tas,data.frame(tas=xp),type="response")
lines(xp,yp,col="green")

m2.fc = glm(dcd ~ fc, family="binomial")
summary(m2.fc)
plot(fc,dcd,ylab="probabilité prédite de décès")
xp=seq(min(fc),max(fc),length=712)
yp=predict(m2.fc,data.frame(fc=xp),type="response")
lines(xp,yp,col="yellow")

#selon toutes les variables explicatives disponibles
m3 = glm(dcd ~ age+tas+fc+glasgow+sexe+chir+inf, family="binomial")
anova(m3,test="Chisq")
summary(m3)

# Sélection descendante des variables explicatives
m3.backward <- step(m3, direction = "backward")
summary(m3.backward)
anova(m3.backward,test="Chisq")
exp(cbind(OR = coef(m3.backward), confint(m3.backward)))

# Etude des valeurs ajustées 
m3.backward$fitted.values
m3.backward$fitted.values[dcd=="0"]
m3.backward$fitted.values[dcd=="1"]
layout(1)
boxplot(m3.backward$fitted.values~dcd)

prob.pred = predict(m3.backward, type="response")
par(mfrow=c(1,2))
hist(prob.pred[dcd==1], probability=T, col='light blue')
lines(density(prob.pred[dcd==1]),col='red',lwd=3)
hist(prob.pred[dcd==0], probability=T, col='light blue')
lines(density(prob.pred[dcd==0]),col='red',lwd=3)

library(ROCR)
pred = prediction(prob.pred, dcd)
perf = performance(pred, "tpr", "fpr")
plot(perf)
AUC=performance(pred, "auc")@y.values[[1]]
AUC

library(rms)
reglog=lrm(dcd ~ age+tas+glasgow+chir)
reglog