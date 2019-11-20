-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: iot_db2
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `PigPrices`
--

DROP TABLE IF EXISTS `PigPrices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PigPrices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `省份` varchar(10) DEFAULT NULL,
  `外三元` float DEFAULT NULL,
  `内三元` float DEFAULT NULL,
  `土杂猪` float DEFAULT NULL,
  `日期` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_PigPrices_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=404 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `animal_keeper`
--

DROP TABLE IF EXISTS `animal_keeper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animal_keeper` (
  `user_id` int(11) DEFAULT NULL,
  `animal_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `animal_id` (`animal_id`),
  CONSTRAINT `animal_keeper_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `animal_keeper_ibfk_2` FOREIGN KEY (`animal_id`) REFERENCES `animals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `animalinfos`
--

DROP TABLE IF EXISTS `animalinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animalinfos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(64) DEFAULT NULL,
  `sick_times` int(11) DEFAULT NULL,
  `total_sick_days` int(11) DEFAULT NULL,
  `total_meters` int(11) DEFAULT NULL,
  `day_meters` int(11) DEFAULT NULL,
  `vaccine_times` int(11) DEFAULT NULL,
  `total_feed_weight` float DEFAULT NULL,
  `total_feed_times` int(11) DEFAULT NULL,
  `total_feed_seconds` int(11) DEFAULT NULL,
  `day_feed_weight` float DEFAULT NULL,
  `day_feed_times` int(11) DEFAULT NULL,
  `day_feed_seconds` int(11) DEFAULT NULL,
  `day_cough_times` int(11) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `health_rate` int(11) DEFAULT NULL,
  `health_status` varchar(6) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `action_status` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_animalinfos_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12011001 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `animals`
--

DROP TABLE IF EXISTS `animals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(18) NOT NULL,
  `birthday` datetime NOT NULL,
  `join_date` datetime NOT NULL,
  `friendly_name` varchar(64) DEFAULT NULL,
  `sex` varchar(2) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `cate_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `camera_id` int(11) DEFAULT NULL,
  `animalinfo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cate_id` (`cate_id`),
  KEY `company_id` (`company_id`),
  KEY `camera_id` (`camera_id`),
  KEY `animalinfo_id` (`animalinfo_id`),
  KEY `ix_animals_id` (`id`),
  KEY `ix_animals_sn` (`sn`),
  CONSTRAINT `animals_ibfk_1` FOREIGN KEY (`cate_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `animals_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `animals_ibfk_3` FOREIGN KEY (`camera_id`) REFERENCES `cameras` (`id`),
  CONSTRAINT `animals_ibfk_4` FOREIGN KEY (`animalinfo_id`) REFERENCES `animalinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12011001 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camerainfos`
--

DROP TABLE IF EXISTS `camerainfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camerainfos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `loc` varchar(64) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `mac` varchar(17) DEFAULT NULL,
  `domain` varchar(10) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  `capacity` text DEFAULT NULL,
  `video_url` varchar(128) DEFAULT NULL,
  `thumb_url` varchar(128) DEFAULT NULL,
  `live_url` varchar(128) DEFAULT NULL,
  `power` float DEFAULT NULL,
  `manufacturers` varchar(18) DEFAULT NULL,
  `manufactures_tel` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_camerainfos_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=600551 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cameras`
--

DROP TABLE IF EXISTS `cameras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cameras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `sn` varchar(20) NOT NULL,
  `friendly_name` varchar(64) DEFAULT NULL,
  `event_id` varchar(255) DEFAULT NULL,
  `entity_id` varchar(255) DEFAULT NULL,
  `state` varchar(10) DEFAULT NULL,
  `attributes` text DEFAULT NULL,
  `last_changed` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `camerainfo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `camerainfo_id` (`camerainfo_id`),
  KEY `ix_cameras_id` (`id`),
  KEY `ix_cameras_sn` (`sn`),
  KEY `cameras_ibfk_2` (`company_id`),
  CONSTRAINT `cameras_ibfk_1` FOREIGN KEY (`camerainfo_id`) REFERENCES `camerainfos` (`id`),
  CONSTRAINT `cameras_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=600551 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_categories_name` (`name`),
  KEY `ix_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `corporate` varchar(64) NOT NULL,
  `scale` varchar(11) DEFAULT NULL,
  `total_scale` int(11) DEFAULT NULL,
  `social_credit_issue` varchar(18) DEFAULT NULL,
  `credit_rate` int(11) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `link` varchar(64) DEFAULT NULL,
  `license_id` int(11) DEFAULT NULL,
  `province` varchar(10) DEFAULT NULL,
  `city` varchar(16) DEFAULT NULL,
  `street_address` varchar(50) DEFAULT NULL,
  `contact` varchar(11) DEFAULT NULL,
  `time` datetime NOT NULL DEFAULT '2019-00-00 00:00:00' ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_companies_id` (`id`),
  KEY `ix_companies_corporate` (`corporate`)
) ENGINE=InnoDB AUTO_INCREMENT=392 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_scope`
--

DROP TABLE IF EXISTS `company_scope`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_scope` (
  `company_id` int(11) DEFAULT NULL,
  `scope_id` int(11) DEFAULT NULL,
  KEY `company_id` (`company_id`),
  KEY `scope_id` (`scope_id`),
  CONSTRAINT `company_scope_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `company_scope_ibfk_2` FOREIGN KEY (`scope_id`) REFERENCES `scopes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `friendly_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_roles_name` (`name`),
  KEY `ix_roles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scopes`
--

DROP TABLE IF EXISTS `scopes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scopes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_scopes_name` (`name`),
  KEY `ix_scopes_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensorinfos`
--

DROP TABLE IF EXISTS `sensorinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensorinfos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `loc` varchar(64) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `mac` varchar(17) DEFAULT NULL,
  `power` float DEFAULT NULL,
  `manufacturers` varchar(18) DEFAULT NULL,
  `manufactures_tel` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_sensorinfos_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=360331 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensors`
--

DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `sn` varchar(20) NOT NULL,
  `friendly_name` varchar(64) DEFAULT NULL,
  `domain` varchar(16) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  `event_id` varchar(255) DEFAULT NULL,
  `entity_id` varchar(250) DEFAULT NULL,
  `state` varchar(60) DEFAULT NULL,
  `attributes` text DEFAULT NULL,
  `last_changed` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `sensorinfo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sensorinfo_id` (`sensorinfo_id`),
  KEY `ix_sensors_sn` (`sn`),
  KEY `ix_sensors_id` (`id`),
  KEY `sensors_ibfk_2` (`company_id`),
  CONSTRAINT `sensors_ibfk_1` FOREIGN KEY (`sensorinfo_id`) REFERENCES `sensorinfos` (`id`),
  CONSTRAINT `sensors_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=360331 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userinfos`
--

DROP TABLE IF EXISTS `userinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userinfos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) NOT NULL,
  `friendly_name` varchar(64) DEFAULT NULL,
  `qq` varchar(11) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `join_datetime` datetime NOT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_userinfos_id` (`id`),
  KEY `ix_userinfos_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12012 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `userinfo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `company_id` (`company_id`),
  KEY `userinfo_id` (`userinfo_id`),
  KEY `ix_users_username` (`username`),
  KEY `ix_users_id` (`id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `users_ibfk_3` FOREIGN KEY (`userinfo_id`) REFERENCES `userinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12012 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `worldmap_latlng`
--

DROP TABLE IF EXISTS `worldmap_latlng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `worldmap_latlng` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lat` float NOT NULL,
  `lng` float NOT NULL,
  `name` varchar(20) CHARACTER SET latin1 NOT NULL,
  `value` float NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `worldmap_latlng_copy`
--

DROP TABLE IF EXISTS `worldmap_latlng_copy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `worldmap_latlng_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lat` float NOT NULL,
  `lng` float NOT NULL,
  `name` varchar(20) CHARACTER SET latin1 NOT NULL,
  `value` float NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-20  3:11:04
