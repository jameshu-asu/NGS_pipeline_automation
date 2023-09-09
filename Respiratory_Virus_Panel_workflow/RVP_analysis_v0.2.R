#!/usr/bin/env Rscript
###Need to edit n<-nR[1:118,2:n] for new table dimensions
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)
library(RColorBrewer)
library(gplots)
library(plyr)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(grid)
library(png)

####Original counts table
mR<-read.delim('RVP_counts_virusOnly.txt', row.names = 1, header = TRUE, sep = ",")

####New counts table
nR<-read.delim('countsTable.txt')
names.1<-read.delim("AccessionToName_RVP.txt")
dim(nR)
n<-nR[1:118,2:length(nR)]
dim(n)
n.1<-as.matrix(n)
rownames(n.1)=names.1$Virus
newtable.1<-rowsum(n.1,row.names(n.1))
for ( col in 1:ncol(newtable.1)){
  colnames(newtable.1)[col] <-  sub("counts.txt", "", colnames(newtable.1)[col])
}
newtable.1<-as.data.frame(newtable.1)
newtable.1<- newtable.1 %>% select(which(!colSums(newtable.1, na.rm=TRUE) %in% 0))

####Merge counts table
mytable = merge(mR, newtable.1, by=0)
dim(mytable)
mytable.1<-as.data.frame(mytable[,2:length(mytable)], row.names=mytable$Row.names)
write.csv(mytable.1,"RVP_counts_virusOnly_updated.txt", quote =FALSE)
mytable.1<-mytable.1[order(rowSums(mytable.1), decreasing=F),]

####metadata and normalization constant creation
dR<-read.delim("RVP_metadata.txt")
dR$Date.2<-as.Date(as.character(dR$Date), format='%y%m%d')
dR$QC<-as.integer(dR$QC)
dR$QC_normalized<-1000000/dR$QC

####Normalize data by multiplying cells with constant
nm1 <- colnames(mytable.1)
newtable.3 <- mytable.1
newtable.3[nm1] <-mytable.1[nm1] * dR$QC_normalized[match(nm1, dR$Respiratory.Seq.ID)][col(newtable.3[nm1])]
write.csv(newtable.3, "RVP_counts_virusOnly_normalized.txt", quote = FALSE)
#newtable.3

