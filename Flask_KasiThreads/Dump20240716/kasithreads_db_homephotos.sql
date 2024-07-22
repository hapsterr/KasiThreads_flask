-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: kasithreads_db
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `homephotos`
--

DROP TABLE IF EXISTS `homephotos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homephotos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `leftphoto` varchar(255) NOT NULL,
  `righttop` varchar(255) NOT NULL,
  `rightbottom` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homephotos`
--

LOCK TABLES `homephotos` WRITE;
/*!40000 ALTER TABLE `homephotos` DISABLE KEYS */;
INSERT INTO `homephotos` VALUES (1,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(2,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(3,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(4,'image3.webp','image3.webp','download (3).jpg'),(5,'image2.jpeg','image2.jpeg','image2.jpeg'),(6,'image1.jpeg','image2.jpeg','download (1).jpg'),(7,'image3.webp','download.jpg','download (3).jpg'),(8,'image2.jpg','image3.webp','download (2).jpg'),(9,'image2.jpeg','image1.jpeg','download (1).jpg'),(10,'image2.jpeg','image2.jpeg','image2.jpeg'),(11,'image3.webp','image2.jpg','image2.jpg'),(12,'image3.webp','image2.jpeg','image1.jpeg'),(13,'image1.jpeg','image1.jpeg','image1.jpeg');
/*!40000 ALTER TABLE `homephotos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-16 12:53:13
