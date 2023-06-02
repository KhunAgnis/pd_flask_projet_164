-- --------------------------------------------------------
-- Hôte :                        localhost
-- Version du serveur:           8.0.31 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Export de la structure de la base pour pereira_daniel_info1a_etam
DROP DATABASE IF EXISTS `pereira_daniel_info1a_etam`;
CREATE DATABASE IF NOT EXISTS `pereira_daniel_info1a_etam` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pereira_daniel_info1a_etam`;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_categorieproduit
DROP TABLE IF EXISTS `t_categorieproduit`;
CREATE TABLE IF NOT EXISTS `t_categorieproduit` (
  `id_Categorie` int NOT NULL AUTO_INCREMENT,
  `nomCategorie` varchar(50) DEFAULT NULL,
  `descCategorie` varchar(50) DEFAULT NULL,
  `imagesCategorie` text,
  PRIMARY KEY (`id_Categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_categorieproduit : ~22 rows (environ)
/*!40000 ALTER TABLE `t_categorieproduit` DISABLE KEYS */;
INSERT INTO `t_categorieproduit` (`id_Categorie`, `nomCategorie`, `descCategorie`, `imagesCategorie`) VALUES
	(1, 'Soutien-gorge', 'Sans coque', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw62f46944/Visuel%20market/SG-MIDNIGHT.jpg?sw=1000&sh=1180&strip=false'),
	(2, 'Soutien-gorge', 'Avec coque', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwf9e03003/653838585_x.jpg?sw=1000&sh=1180&strip=false'),
	(3, 'Soutien-gorge', 'Push-up', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwd8bbb1b7/653575781_x.jpg?sw=1000&sh=1180&strip=false'),
	(4, 'Soutien-gorge', 'Bandeaux', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw6d5d7209/653575881_x.jpg?sw=1000&sh=1180&strip=false'),
	(5, 'Soutien-gorge', 'Corbeille', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw47ebd800/653917780_x.jpg?sw=1000&sh=1180&strip=false'),
	(6, 'Culotte', 'Menstruelle', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwc892192e/652889405_6.jpg?sw=1000&sh=1180&strip=false'),
	(7, 'Culotte', 'Shortys', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw28dde847/651450780_x.jpg?sw=1000&sh=1180&strip=false'),
	(8, 'Culotte', 'Tanga', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw70f4b6ee/653068805_x.jpg?sw=1000&sh=1180&strip=false'),
	(9, 'Culotte', 'String', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw327b756a/653913780_x.jpg?sw=1000&sh=1180&strip=false'),
	(10, 'Culotte', 'Hipsters', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw4a28272f/652455170_x.jpg?sw=1000&sh=1180&strip=false'),
	(11, 'Culotte', 'Shapewear', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw3e4cc3f1/652441383_x.jpg?sw=1000&sh=1180&strip=false'),
	(12, 'Lingerie', 'Body', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwc57dc5d8/653723105_x.jpg?sw=1000&sh=1180&strip=false'),
	(13, 'Lingerie', 'Porte-jartelles', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwce733cd1/653819878_x.jpg?sw=1000&sh=1180&strip=false'),
	(14, 'Lingerie', 'Collants', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw1ddc0f8d/652583405_c.jpg?sw=1000&sh=1180&strip=false'),
	(15, 'Maillot de bain', '2 pièces', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwe22b8bc2/Visuel%20market/010_ETAM%20050423_508-V2-CMJN.jpg?sw=1000&sh=1180&strip=false'),
	(16, 'Maillot de bain', '1 pièce', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw68f0ef51/653978105_x.jpg?sw=1000&sh=1180&strip=false'),
	(17, 'Maillot de bain', 'Beachwear', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwfc613191/653922168_x.jpg?sw=1000&sh=1180&strip=false'),
	(18, 'Pyjama', 'Nuisette', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw6cecdc76/653789701_x.jpg?sw=1000&sh=1180&strip=false'),
	(19, 'Pyjama', 'Chemise de nuit', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwc6fd783d/653957870_c.jpg?sw=1000&sh=1180&strip=false'),
	(20, 'Pyjama', 'Déshabillé/Kimono', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw302a071e/653665673_x.jpg?sw=1000&sh=1180&strip=false'),
	(21, 'Pyjama', 'Bas de pyjama', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw0548802e/653948580_x.jpg?sw=1000&sh=1180&strip=false'),
	(22, 'Pyjama', 'Haut de pyjama', 'https://www.etam.ch/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dwacf8ce65/653893546_x.jpg?sw=1000&sh=1180&strip=false');
/*!40000 ALTER TABLE `t_categorieproduit` ENABLE KEYS */;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_couleur
DROP TABLE IF EXISTS `t_couleur`;
CREATE TABLE IF NOT EXISTS `t_couleur` (
  `id_Couleur` int NOT NULL AUTO_INCREMENT,
  `couleur` varchar(50) NOT NULL,
  PRIMARY KEY (`id_Couleur`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_couleur : ~15 rows (environ)
/*!40000 ALTER TABLE `t_couleur` DISABLE KEYS */;
INSERT INTO `t_couleur` (`id_Couleur`, `couleur`) VALUES
	(1, 'Noir'),
	(2, 'Blanc'),
	(3, 'Rouge'),
	(4, 'Bleu ciel'),
	(5, 'Bleu'),
	(6, 'Ecru'),
	(7, 'Bordeau'),
	(8, 'Vert'),
	(9, 'Bleu foncé'),
	(10, 'Beige'),
	(11, 'Blush'),
	(12, 'Rose bonbon'),
	(13, 'Rose'),
	(14, 'Emeraude'),
	(15, 'Kaki');
/*!40000 ALTER TABLE `t_couleur` ENABLE KEYS */;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_produit
DROP TABLE IF EXISTS `t_produit`;
CREATE TABLE IF NOT EXISTS `t_produit` (
  `id_Produit` int NOT NULL AUTO_INCREMENT,
  `tailleProduit` varchar(50) DEFAULT NULL,
  `nomProduit` varchar(50) DEFAULT NULL,
  `fk_Couleur` int DEFAULT NULL,
  `fk_Categorie` int NOT NULL,
  PRIMARY KEY (`id_Produit`),
  KEY `FKProduitCategorie` (`fk_Categorie`),
  KEY `fk_Couleur` (`fk_Couleur`),
  CONSTRAINT `FKProduitCategorie` FOREIGN KEY (`fk_Categorie`) REFERENCES `t_categorieproduit` (`id_Categorie`),
  CONSTRAINT `FKProduitCouleur` FOREIGN KEY (`fk_Couleur`) REFERENCES `t_couleur` (`id_Couleur`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_produit : ~12 rows (environ)
/*!40000 ALTER TABLE `t_produit` DISABLE KEYS */;
INSERT INTO `t_produit` (`id_Produit`, `tailleProduit`, `nomProduit`, `fk_Couleur`, `fk_Categorie`) VALUES
	(1, 'M', 'Pantalon de pyjama imprimé', 5, 21),
	(2, 'L', 'Pantalon de pyjama imprimé', 5, 21),
	(3, 'M', 'Pantalon de pyjama imprimé', 1, 21),
	(4, 'L', 'Pantalon de pyjama imprimé', 1, 21),
	(5, '70B', 'Soutien-gorge corbeille', 6, 5),
	(6, '70B', 'Soutien-gorge corbeille', 4, 5),
	(7, '75B', 'Soutien-gorge corbeille', 6, 5),
	(8, '75B', 'Soutien-gorge corbeille', 4, 5),
	(9, '32', 'String en brodé', 12, 9),
	(10, '34', 'String en brodé', 14, 9),
	(11, '36', 'String en brodé', 3, 9),
	(12, '38', 'String en brodé', 1, 9);
/*!40000 ALTER TABLE `t_produit` ENABLE KEYS */;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_produitajoutstock
DROP TABLE IF EXISTS `t_produitajoutstock`;
CREATE TABLE IF NOT EXISTS `t_produitajoutstock` (
  `id_ProduitAjoutStock` int NOT NULL AUTO_INCREMENT,
  `DateAjout` date NOT NULL,
  `QuantiteAjoute` int NOT NULL,
  `fk_Stock` int NOT NULL,
  `fk_Produit` int NOT NULL,
  PRIMARY KEY (`id_ProduitAjoutStock`),
  KEY `FK_ProduitAjoutStock_Produit` (`fk_Produit`),
  KEY `FK_ProduitAjoutStock_Stock` (`fk_Stock`),
  CONSTRAINT `FK_ProduitAjoutStock_Produit` FOREIGN KEY (`fk_Produit`) REFERENCES `t_produit` (`id_Produit`),
  CONSTRAINT `FK_ProduitAjoutStock_Stock` FOREIGN KEY (`fk_Stock`) REFERENCES `t_stock` (`id_Stock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_produitajoutstock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_produitajoutstock` DISABLE KEYS */;
INSERT INTO `t_produitajoutstock` (`id_ProduitAjoutStock`, `DateAjout`, `QuantiteAjoute`, `fk_Stock`, `fk_Produit`) VALUES
	(1, '2023-05-25', 100, 1, 2);
/*!40000 ALTER TABLE `t_produitajoutstock` ENABLE KEYS */;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_produitretirerstock
DROP TABLE IF EXISTS `t_produitretirerstock`;
CREATE TABLE IF NOT EXISTS `t_produitretirerstock` (
  `id_ProduitRetirerStock` int NOT NULL AUTO_INCREMENT,
  `DateRetirer` date NOT NULL,
  `QuantiteRetirer` int NOT NULL,
  `fk_Stock` int NOT NULL,
  `fk_Produit` int NOT NULL,
  PRIMARY KEY (`id_ProduitRetirerStock`),
  KEY `FK_ProduitRetirerStock_Produit` (`fk_Produit`),
  KEY `FK_ProduitRetirerStock_Stock` (`fk_Stock`),
  CONSTRAINT `FK_ProduitRetirerStock_Produit` FOREIGN KEY (`fk_Produit`) REFERENCES `t_produit` (`id_Produit`),
  CONSTRAINT `FK_ProduitRetirerStock_Stock` FOREIGN KEY (`fk_Stock`) REFERENCES `t_stock` (`id_Stock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_produitretirerstock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_produitretirerstock` DISABLE KEYS */;
INSERT INTO `t_produitretirerstock` (`id_ProduitRetirerStock`, `DateRetirer`, `QuantiteRetirer`, `fk_Stock`, `fk_Produit`) VALUES
	(1, '2021-05-24', 5, 1, 2);
/*!40000 ALTER TABLE `t_produitretirerstock` ENABLE KEYS */;

-- Export de la structure de la table pereira_daniel_info1a_etam. t_stock
DROP TABLE IF EXISTS `t_stock`;
CREATE TABLE IF NOT EXISTS `t_stock` (
  `id_Stock` int NOT NULL AUTO_INCREMENT,
  `quantiteStock` int DEFAULT NULL,
  `lieuStock` varchar(50) NOT NULL,
  `dernieredateajout` date DEFAULT NULL,
  `fk_Produit` int NOT NULL,
  PRIMARY KEY (`id_Stock`),
  KEY `FKProduitStock` (`fk_Produit`),
  CONSTRAINT `FKProduitStock` FOREIGN KEY (`fk_Produit`) REFERENCES `t_produit` (`id_Produit`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table pereira_daniel_info1a_etam.t_stock : ~12 rows (environ)
/*!40000 ALTER TABLE `t_stock` DISABLE KEYS */;
INSERT INTO `t_stock` (`id_Stock`, `quantiteStock`, `lieuStock`, `dernieredateajout`, `fk_Produit`) VALUES
	(1, 30, 'Garage', '2023-05-30', 1),
	(2, 30, 'Garage', '2023-05-30', 2),
	(3, 30, 'Garage', '2023-05-30', 3),
	(4, 30, 'Garage', '2023-05-30', 4),
	(5, 15, 'Arrière-boutique', '2023-05-30', 5),
	(6, 15, 'Arrière-boutique', '2023-05-30', 6),
	(7, 15, 'Arrière-boutique', '2023-05-30', 7),
	(8, 15, 'Arrière-boutique', '2023-05-30', 8),
	(9, 10, 'Rayon', '2023-05-30', 9),
	(10, 10, 'Rayon', '2023-05-30', 10),
	(11, 10, 'Rayon', '2023-05-30', 11),
	(12, 10, 'Rayon', '2023-05-30', 12);
/*!40000 ALTER TABLE `t_stock` ENABLE KEYS */;

-- Export de la structure de déclencheur pereira_daniel_info1a_etam. tr_ajout_stock
DROP TRIGGER IF EXISTS `tr_ajout_stock`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tr_ajout_stock` AFTER INSERT ON `t_produitajoutstock` FOR EACH ROW BEGIN
  UPDATE t_stock
  SET quantiteStock = quantiteStock + NEW.QuantiteAjoute
  WHERE fk_Produit = NEW.fk_Produit;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Export de la structure de déclencheur pereira_daniel_info1a_etam. tr_retirer_stock
DROP TRIGGER IF EXISTS `tr_retirer_stock`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tr_retirer_stock` AFTER INSERT ON `t_produitretirerstock` FOR EACH ROW BEGIN
  UPDATE t_stock
  SET quantiteStock = quantiteStock - NEW.QuantiteRetirer
  WHERE fk_Produit = NEW.fk_Produit;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
