-- --------------------------------------------------------
-- Hôte :                        localhost
-- Version du serveur:           5.7.24 - MySQL Community Server (GPL)
-- SE du serveur:                Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Listage de la structure de la base pour mydb
DROP DATABASE IF EXISTS `mydb`;
CREATE DATABASE IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mydb`;

-- Listage de la structure de la table mydb. academy_awards
DROP TABLE IF EXISTS `academy_awards`;
CREATE TABLE IF NOT EXISTS `academy_awards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `movies_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`,`movies_id`),
  KEY `fk_academy_awards_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_academy_awards_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. account
DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `uuid` varchar(32) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. account_has_countries
DROP TABLE IF EXISTS `account_has_countries`;
CREATE TABLE IF NOT EXISTS `account_has_countries` (
  `account_uuid` varchar(32) NOT NULL,
  `countries_id` int(11) NOT NULL,
  PRIMARY KEY (`account_uuid`,`countries_id`),
  KEY `fk_account_has_countries_countries1_idx` (`countries_id`),
  CONSTRAINT `fk_account_has_countries_account1` FOREIGN KEY (`account_uuid`) REFERENCES `account` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_account_has_countries_countries1` FOREIGN KEY (`countries_id`) REFERENCES `countries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. actors
DROP TABLE IF EXISTS `actors`;
CREATE TABLE IF NOT EXISTS `actors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. consumptions
DROP TABLE IF EXISTS `consumptions`;
CREATE TABLE IF NOT EXISTS `consumptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `movies_id` int(11) NOT NULL,
  `Account_idAccount` varchar(32) NOT NULL,
  PRIMARY KEY (`id`,`movies_id`,`Account_idAccount`),
  KEY `fk_netflix_diffusions_movies1_idx` (`movies_id`),
  KEY `fk_netflix_diffusions_Account1_idx` (`Account_idAccount`),
  CONSTRAINT `fk_netflix_diffusions_Account1` FOREIGN KEY (`Account_idAccount`) REFERENCES `account` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_netflix_diffusions_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. countries
DROP TABLE IF EXISTS `countries`;
CREATE TABLE IF NOT EXISTS `countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. directors
DROP TABLE IF EXISTS `directors`;
CREATE TABLE IF NOT EXISTS `directors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `nationality` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. directors_has_nationalities
DROP TABLE IF EXISTS `directors_has_nationalities`;
CREATE TABLE IF NOT EXISTS `directors_has_nationalities` (
  `directors_id` int(11) NOT NULL,
  `nationalities_id` int(11) NOT NULL,
  PRIMARY KEY (`directors_id`,`nationalities_id`),
  KEY `fk_directors_has_nationalities_nationalities1_idx` (`nationalities_id`),
  KEY `fk_directors_has_nationalities_directors1_idx` (`directors_id`),
  CONSTRAINT `fk_directors_has_nationalities_directors1` FOREIGN KEY (`directors_id`) REFERENCES `directors` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_directors_has_nationalities_nationalities1` FOREIGN KEY (`nationalities_id`) REFERENCES `nationalities` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. festivals
DROP TABLE IF EXISTS `festivals`;
CREATE TABLE IF NOT EXISTS `festivals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `year` datetime NOT NULL,
  `countries_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`countries_id`),
  KEY `fk_festivals_countries1_idx` (`countries_id`),
  CONSTRAINT `fk_festivals_countries1` FOREIGN KEY (`countries_id`) REFERENCES `countries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. festival_selection_names
DROP TABLE IF EXISTS `festival_selection_names`;
CREATE TABLE IF NOT EXISTS `festival_selection_names` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `festivals_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`festivals_id`),
  KEY `fk_festival_selection_names_festivals1_idx` (`festivals_id`),
  CONSTRAINT `fk_festival_selection_names_festivals1` FOREIGN KEY (`festivals_id`) REFERENCES `festivals` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. languages
DROP TABLE IF EXISTS `languages`;
CREATE TABLE IF NOT EXISTS `languages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies
DROP TABLE IF EXISTS `movies`;
CREATE TABLE IF NOT EXISTS `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `type` int(11) DEFAULT NULL COMMENT 'enum: {movie: 0, serie: 1}',
  `description` varchar(45) DEFAULT NULL,
  `released_at` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `image` longtext,
  `movie_types_id` int(11) NOT NULL,
  `netflix_id` int(11) DEFAULT NULL,
  `imdb_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`movie_types_id`),
  KEY `fk_movies_movie_types1_idx` (`movie_types_id`),
  CONSTRAINT `fk_movies_movie_types1` FOREIGN KEY (`movie_types_id`) REFERENCES `movie_types` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_actors
DROP TABLE IF EXISTS `movies_has_actors`;
CREATE TABLE IF NOT EXISTS `movies_has_actors` (
  `movies_id` int(11) NOT NULL,
  `actors_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`actors_id`),
  KEY `fk_movies_has_actors_actors1_idx` (`actors_id`),
  KEY `fk_movies_has_actors_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_actors_actors1` FOREIGN KEY (`actors_id`) REFERENCES `actors` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_actors_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_countries
DROP TABLE IF EXISTS `movies_has_countries`;
CREATE TABLE IF NOT EXISTS `movies_has_countries` (
  `movies_id` int(11) NOT NULL,
  `countries_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`countries_id`),
  KEY `fk_movies_has_countries_countries1_idx` (`countries_id`),
  KEY `fk_movies_has_countries_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_countries_countries1` FOREIGN KEY (`countries_id`) REFERENCES `countries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_countries_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_directors
DROP TABLE IF EXISTS `movies_has_directors`;
CREATE TABLE IF NOT EXISTS `movies_has_directors` (
  `movies_id` int(11) NOT NULL,
  `directors_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`directors_id`),
  KEY `fk_movies_has_directors_directors1_idx` (`directors_id`),
  KEY `fk_movies_has_directors_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_directors_directors1` FOREIGN KEY (`directors_id`) REFERENCES `directors` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_directors_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_festivals
DROP TABLE IF EXISTS `movies_has_festivals`;
CREATE TABLE IF NOT EXISTS `movies_has_festivals` (
  `movies_id` int(11) NOT NULL,
  `festivals_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`festivals_id`),
  KEY `fk_movies_has_festivals_festivals1_idx` (`festivals_id`),
  KEY `fk_movies_has_festivals_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_festivals_festivals1` FOREIGN KEY (`festivals_id`) REFERENCES `festivals` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_festivals_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_languages
DROP TABLE IF EXISTS `movies_has_languages`;
CREATE TABLE IF NOT EXISTS `movies_has_languages` (
  `movies_id` int(11) NOT NULL,
  `languages_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`languages_id`),
  KEY `fk_movies_has_languages_languages1_idx` (`languages_id`),
  KEY `fk_movies_has_languages_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_languages_languages1` FOREIGN KEY (`languages_id`) REFERENCES `languages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_languages_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movies_has_nationalities
DROP TABLE IF EXISTS `movies_has_nationalities`;
CREATE TABLE IF NOT EXISTS `movies_has_nationalities` (
  `movies_id` int(11) NOT NULL,
  `nationalities_id` int(11) NOT NULL,
  PRIMARY KEY (`movies_id`,`nationalities_id`),
  KEY `fk_movies_has_nationalities_nationalities1_idx` (`nationalities_id`),
  KEY `fk_movies_has_nationalities_movies1_idx` (`movies_id`),
  CONSTRAINT `fk_movies_has_nationalities_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_nationalities_nationalities1` FOREIGN KEY (`nationalities_id`) REFERENCES `nationalities` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. movie_types
DROP TABLE IF EXISTS `movie_types`;
CREATE TABLE IF NOT EXISTS `movie_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT 'serie, movie…',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. nationalities
DROP TABLE IF EXISTS `nationalities`;
CREATE TABLE IF NOT EXISTS `nationalities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table mydb. recommandations
DROP TABLE IF EXISTS `recommandations`;
CREATE TABLE IF NOT EXISTS `recommandations` (
  `idReco` int(11) NOT NULL,
  `movies_id` int(11) NOT NULL,
  `thumb_X` int(10) unsigned DEFAULT NULL,
  `thumb_Y` int(10) unsigned DEFAULT NULL,
  `thumb_Z` int(10) unsigned DEFAULT NULL,
  `account_uuid` varchar(32) NOT NULL,
  PRIMARY KEY (`idReco`,`movies_id`,`account_uuid`),
  KEY `fk_netflix_home_page_rankings_has_movies_movies1_idx` (`movies_id`),
  KEY `fk_film_ranking_account1_idx` (`account_uuid`),
  CONSTRAINT `fk_film_ranking_account1` FOREIGN KEY (`account_uuid`) REFERENCES `account` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_netflix_home_page_rankings_has_movies_movies1` FOREIGN KEY (`movies_id`) REFERENCES `movies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Les données exportées n'étaient pas sélectionnées.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
