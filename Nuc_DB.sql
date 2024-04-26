-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: nuc_db
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cellules`
--

DROP TABLE IF EXISTS `cellules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cellules` (
  `CelluleID` int NOT NULL,
  `Nom` varchar(64) DEFAULT NULL,
  `ChassisID` int DEFAULT NULL,
  `Position` int DEFAULT NULL,
  PRIMARY KEY (`CelluleID`),
  KEY `ChassisID` (`ChassisID`),
  CONSTRAINT `cellules_ibfk_1` FOREIGN KEY (`ChassisID`) REFERENCES `chassis` (`ChassisID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cellules`
--

LOCK TABLES `cellules` WRITE;
/*!40000 ALTER TABLE `cellules` DISABLE KEYS */;
INSERT INTO `cellules` VALUES (1,'Pelton',1,1),(2,'Vivarium',1,2),(3,'Pecheur',1,3),(5,'CuZn',1,4),(6,'Eolienne',2,1),(7,'Petite Dixence',2,2),(9,'Valais',2,3),(10,'Tornade',2,4),(11,'Centrale thermique',3,1),(12,'Systeme solaire',3,2),(13,'Centrale solaire',NULL,NULL);
/*!40000 ALTER TABLE `cellules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chassis`
--

DROP TABLE IF EXISTS `chassis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chassis` (
  `ChassisID` int NOT NULL AUTO_INCREMENT,
  `IP` varchar(16) DEFAULT NULL,
  `NbCellules` int DEFAULT NULL,
  PRIMARY KEY (`ChassisID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chassis`
--

LOCK TABLES `chassis` WRITE;
/*!40000 ALTER TABLE `chassis` DISABLE KEYS */;
INSERT INTO `chassis` VALUES (1,'172.16.0.3',4),(2,'172.16.0.4',4),(3,'172.16.0.5',2);
/*!40000 ALTER TABLE `chassis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `options` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `multi` tinyint(1) DEFAULT NULL,
  `billes` float(8,2) DEFAULT NULL,
  `temps` float(8,2) DEFAULT NULL,
  `Unite` text,
  `Mode infini` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `options`
--

LOCK TABLES `options` WRITE;
/*!40000 ALTER TABLE `options` DISABLE KEYS */;
INSERT INTO `options` VALUES (55,0,38.00,60.00,'m',0);
/*!40000 ALTER TABLE `options` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-26 15:39:39
