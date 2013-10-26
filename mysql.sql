-- MySQL dump 10.14  Distrib 10.0.4-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fjospidie
-- ------------------------------------------------------
-- Server version	10.0.4-MariaDB-1~wheezy-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alert`
--

DROP TABLE IF EXISTS `alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alert` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `report_id` mediumint(9) NOT NULL,
  `alarm_text` blob,
  `classification` blob,
  `priority` int(11) DEFAULT NULL,
  `protocol` varchar(10) DEFAULT NULL,
  `from_ip` blob,
  `to_ip` blob,
  PRIMARY KEY (`id`),
  KEY `FK_report_id` (`report_id`),
  CONSTRAINT `FK_report_id` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2187 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `download`
--

DROP TABLE IF EXISTS `download`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `download` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `report_id` mediumint(9) NOT NULL,
  `data` longblob,
  `md5` blob,
  `sha1` blob,
  `sha256` blob,
  `filename` blob,
  `size` mediumtext,
  `uuid` blob,
  PRIMARY KEY (`id`),
  KEY `fk_download_report` (`report_id`),
  CONSTRAINT `fk_download_report` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entry`
--

DROP TABLE IF EXISTS `entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `report_id` mediumint(9) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_entry_id` (`report_id`),
  CONSTRAINT `fk_entry_id` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=635806 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `graph`
--

DROP TABLE IF EXISTS `graph`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `graph` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `report_id` mediumint(9) NOT NULL,
  `graph` mediumblob,
  PRIMARY KEY (`id`),
  KEY `FK_report_id_graph` (`report_id`),
  CONSTRAINT `FK_report_id_graph` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2275 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `header`
--

DROP TABLE IF EXISTS `header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `header` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entry_id` mediumint(9) NOT NULL,
  `name` blob NOT NULL,
  `value` blob NOT NULL,
  `type` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_entry_header` (`entry_id`),
  CONSTRAINT `fk_entry_header` FOREIGN KEY (`entry_id`) REFERENCES `entry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8694389 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pcap`
--

DROP TABLE IF EXISTS `pcap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pcap` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `report_id` mediumint(9) DEFAULT NULL,
  `data` longblob,
  `uuid` blob,
  PRIMARY KEY (`id`),
  KEY `fk_pcap_report` (`report_id`),
  CONSTRAINT `fk_pcap_report` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2306 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `url` blob,
  `starttime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `endtime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `report_uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=2425 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `request` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `entry_id` mediumint(9) NOT NULL,
  `bodySize` int(11) DEFAULT NULL,
  `headerSize` int(11) DEFAULT NULL,
  `method` varchar(20) DEFAULT NULL,
  `uri` blob,
  `httpVersion` blob,
  `host` blob,
  `port` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_request_id` (`entry_id`),
  CONSTRAINT `fk_request_id` FOREIGN KEY (`entry_id`) REFERENCES `entry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=634597 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `response` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `entry_id` mediumint(9) NOT NULL,
  `httpVersion` blob,
  `statusText` blob,
  `status` int(11) DEFAULT NULL,
  `bodySize` int(11) DEFAULT NULL,
  `headerSize` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_response_id` (`entry_id`),
  CONSTRAINT `fk_response_id` FOREIGN KEY (`entry_id`) REFERENCES `entry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=634598 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-26 21:23:26
