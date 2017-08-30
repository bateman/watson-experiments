require("ggplot2")
setwd("C:\\Users\\Fabio\\Documents\\GitHub\\watson-experiments")
w <- read.csv(file="./aalmiray.csv", head=TRUE, sep=";")

w$m <- mean(w$agreeableness)

ggplot(data=w, aes(x=year.month, y=agreeableness, group = 1)) + 
  geom_point(size=2) + 
  geom_line(size=1) + 
  labs(x = "", y = "agreeableness")+
  #geom_text(aes(label=agreeableness), hjust=-0.2, vjust=1) + 
  theme_bw()

ggplot(data=w, aes(x=year.month, group = 1)) + 
  geom_line(aes(y = agreeableness)) + 
  geom_line(aes(y = m)) +
  labs(x = "", y = "agreeableness")+
  theme_bw() + theme(axis.text.x = element_text(angle = 45, hjust = 1))
