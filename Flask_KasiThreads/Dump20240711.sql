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
-- Table structure for table `brandlogo`
--

DROP TABLE IF EXISTS `brandlogo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brandlogo` (
  `logo_id` int NOT NULL AUTO_INCREMENT,
  `brand_id` int DEFAULT NULL,
  `logopath` varchar(255) NOT NULL,
  PRIMARY KEY (`logo_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `brandlogo_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brandlogo`
--

LOCK TABLES `brandlogo` WRITE;
/*!40000 ALTER TABLE `brandlogo` DISABLE KEYS */;
INSERT INTO `brandlogo` VALUES (3,16,'image3.webp'),(4,17,'1-nike-logo-design-–-history-meaning-and-evolution.webp'),(5,18,'image2.jpeg'),(6,19,'image1.jpeg');
/*!40000 ALTER TABLE `brandlogo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(10) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'HL','SEOKETSA','happyseoketsa@gmail.com','0646148836','$2b$12$gn2PFqnyD7w3QjV.nUD5ruQGdhdpO1J7IWMpJGZO6TmBUhBKBV1FO','2024-07-11 14:44:56');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homephotos`
--

LOCK TABLES `homephotos` WRITE;
/*!40000 ALTER TABLE `homephotos` DISABLE KEYS */;
INSERT INTO `homephotos` VALUES (1,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(2,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(3,'<FileStorage: \'image3.webp\' (\'image/webp\')>','<FileStorage: \'download.jpg\' (\'image/jpeg\')>','<FileStorage: \'download (2).jpg\' (\'image/jpeg\')>'),(4,'image3.webp','image3.webp','download (3).jpg'),(5,'image2.jpeg','image2.jpeg','image2.jpeg');
/*!40000 ALTER TABLE `homephotos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `filename` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `sizes` text NOT NULL,
  `type` text NOT NULL,
  `brand` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (2,'AIR FORCE','THIS IS AN AIRFORCE','download (1).jpg',1000,'UK 1,UK 2','shoes','kasithreadsss'),(3,'AIR FORCE','THIS IS AN AIRFORCE','download (1).jpg',1000,'','shoes','kasithreadsss'),(4,'AIR FORCE','THIS IS AN AIRFORCE','download (1).jpg',1000,'','shoes','kasithreadsss'),(5,'AIR FORCE','THIS IS AN AIRFORCE','download (1).jpg',1000,'','shoes','kasithreadsss'),(6,'AIR FORCE','THIS IS AN AIRFORCE','download (1).jpg',1000,'','shoes','kasithreadsss'),(7,'AIR FORCE','ohjfbd;sogihrdwukgjlierwhgwer','download (3).jpg',100,'UK 2','shoes','nikee');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brandname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `user_type` enum('admin','brandowner') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`brandname`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'kasithreadss','happyseoketsa@gmail.com','$2b$12$DOKuwXDK6i5MXtL573BB/Ozid.vrIUtIwNKFwI0EITnNRNdQQBqVG','admin'),(5,'Happy','happyseoketsa@gmail.com','$2b$12$odQhFVURY418C6fmdvw9t.vqbb2NFro215YHWftbmnF0jCdmVwqu.','admin'),(6,'kasithreadsss','happyseoketsa@gmail.com','$2b$12$gYY7vSJlMAFN4WA8XkqOv.nVNhsWlb3zsplj1cFPUnJrCBqnPo4hO','admin'),(7,'happyy','happyseoketsa@gmail.com','$2b$12$VBfeCWKetWf7ezUxPpis7u3TvXgxobIgsAyUztINa.I8mCcZBblCi','brandowner'),(13,'nike','happyseoketsa@gmail.com','$2b$12$EGpMp9sPQJrKgABMM5YdRuPf1q2A4hn5WhoY74rZhDPmg8BC4Sxu6','brandowner'),(15,'puma','happyseoketsa@gmail.com','$2b$12$NDKXzUtbz4w.s2v3Q5dErOkKJvCyAsuePFYgHSvUDlyAJCDMnctmG','brandowner'),(16,'adidas','happyseoketsa@gmail.com','$2b$12$2YAg.01LgiVf653tJRgXue3xLOIDMeQu2amOWPDAyo6maQ3izRo/q','brandowner'),(17,'nikee','happyseoketsa@gmail.com','$2b$12$xEgNDrp9BTLYEGp6GdOmeuky02ogoGCFZ7GBy2/1fkDqR2c6OTEWu','brandowner'),(18,'Ngenge','happyseoketsa@gmail.com','$2b$12$PdKOalHSMhiku8gcLevRAeZhiRMpGhEa0bZotr4xAtt.DfUm.IN/u','admin'),(19,'Lesego','kasithreads31@gmail.com','$2b$12$iEV8H9IhnjnVrKPkKHktVuRfDkcJCuz/wdrBnr.dU/944VkikLn4W','brandowner');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-11 17:44:46
