-- MySQL Script generated by MySQL Workbench
-- Sat Jun 18 22:40:41 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema naver_movie
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema naver_movie
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `naver_movie` DEFAULT CHARACTER SET utf8 ;
USE `naver_movie` ;

-- -----------------------------------------------------
-- Table `naver_movie`.`movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`movie` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`movie` (
  `movie_code` INT NOT NULL,
  `film_rate_kor` VARCHAR(45) NULL,
  `film_rate_foreign` VARCHAR(45) NULL,
  `story` TEXT NULL,
  `makingnote` TEXT NULL,
  `aka` VARCHAR(45) NULL,
  `title_kor` VARCHAR(45) NULL,
  `title_foreign` VARCHAR(45) NULL,
  `release_date` VARCHAR(45) NULL,
  `current_opening` VARCHAR(45) NULL,
  `img_url` VARCHAR(300) NULL,
  `running_time` VARCHAR(45) NULL,
  `cumulate_audience` VARCHAR(45) NULL,
  PRIMARY KEY (`movie_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `naver_movie`.`peoole`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`peoole` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`peoole` (
  `people_code` INT NOT NULL,
  `thumbnail` VARCHAR(200) NULL,
  `name` VARCHAR(90) NULL,
  `eng_name` VARCHAR(90) NULL,
  PRIMARY KEY (`people_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `naver_movie`.`movie_appearance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`movie_appearance` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`movie_appearance` (
  `people_code` INT NOT NULL,
  `movie_code` INT NOT NULL,
  `role` VARCHAR(45) NULL,
  PRIMARY KEY (`people_code`, `movie_code`),
  CONSTRAINT `fk_movie_appearance_mpeoole`
    FOREIGN KEY (`people_code`)
    REFERENCES `naver_movie`.`peoole` (`people_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_appearance_movie1`
    FOREIGN KEY (`movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_movie_appearance_mpeoole_idx` ON `naver_movie`.`movie_appearance` (`people_code` ASC) VISIBLE;

CREATE INDEX `fk_movie_appearance_movie1_idx` ON `naver_movie`.`movie_appearance` (`movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.` quotes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.` quotes` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.` quotes` (
  `quotes_id` INT NOT NULL AUTO_INCREMENT,
  `peoole_code` INT NOT NULL,
  `movie_code` INT NOT NULL,
  `quotes` TEXT NULL,
  `good` INT NULL,
  `userid` VARCHAR(20) NULL,
  PRIMARY KEY (`quotes_id`, `peoole_code`, `movie_code`),
  CONSTRAINT `fk_ quotes_movie_appearance1`
    FOREIGN KEY (`peoole_code` , `movie_code`)
    REFERENCES `naver_movie`.`movie_appearance` (`people_code` , `movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_ quotes_movie_appearance1_idx` ON `naver_movie`.` quotes` (`peoole_code` ASC, `movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`casting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`casting` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`casting` (
  `casting_id` INT NOT NULL AUTO_INCREMENT,
  `people_code` INT NOT NULL,
  `movie_code` INT NOT NULL,
  `casting_name` VARCHAR(45) NULL,
  PRIMARY KEY (`casting_id`, `people_code`, `movie_code`),
  CONSTRAINT `fk_casting_movie_appearance1`
    FOREIGN KEY (`people_code` , `movie_code`)
    REFERENCES `naver_movie`.`movie_appearance` (`people_code` , `movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_casting_movie_appearance1_idx` ON `naver_movie`.`casting` (`people_code` ASC, `movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`mpeople_sub`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`mpeople_sub` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`mpeople_sub` (
  `mpeople_sub_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `casting` VARCHAR(45) NULL,
  PRIMARY KEY (`mpeople_sub_id`, `movie_movie_code`),
  CONSTRAINT `fk_mpeople_sub_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_mpeople_sub_movie1_idx` ON `naver_movie`.`mpeople_sub` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`relate_movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`relate_movie` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`relate_movie` (
  `movie_movie_code` INT NOT NULL,
  `movie_movie_code1` INT NOT NULL,
  PRIMARY KEY (`movie_movie_code`, `movie_movie_code1`),
  CONSTRAINT `fk_movie_has_movie_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_has_movie_movie2`
    FOREIGN KEY (`movie_movie_code1`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_movie_has_movie_movie2_idx` ON `naver_movie`.`relate_movie` (`movie_movie_code1` ASC) VISIBLE;

CREATE INDEX `fk_movie_has_movie_movie1_idx` ON `naver_movie`.`relate_movie` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`comment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`comment` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`comment` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `score` INT NULL,
  `comment` TEXT NULL,
  `type` VARCHAR(45) NULL,
  `write_time` VARCHAR(45) NULL,
  `good` INT NULL,
  `bad` INT NULL,
  PRIMARY KEY (`comment_id`, `movie_movie_code`),
  CONSTRAINT `fk_score_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_score_movie1_idx` ON `naver_movie`.`comment` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`review`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`review` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`review` (
  `review_id` INT NOT NULL,
  `movie_movie_code` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  `view_num` INT NULL,
  `good` INT NULL,
  `date` VARCHAR(45) NULL,
  `writer` VARCHAR(45) NULL,
  `contents` TEXT NULL,
  PRIMARY KEY (`review_id`, `movie_movie_code`),
  CONSTRAINT `fk_review_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_review_movie1_idx` ON `naver_movie`.`review` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`score`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`score` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`score` (
  `score_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `score` DOUBLE NULL,
  `type` VARCHAR(45) NULL,
  `comment_number` INT NULL,
  PRIMARY KEY (`score_id`, `movie_movie_code`),
  CONSTRAINT `fk_score_movie2`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_score_movie2_idx` ON `naver_movie`.`score` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`review_comment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`review_comment` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`review_comment` (
  `reviewcomment_id` INT NOT NULL AUTO_INCREMENT,
  `review_review_id` INT NOT NULL,
  `review_movie_movie_code` INT NOT NULL,
  `writer` VARCHAR(45) NULL,
  `good` INT NULL,
  `bad` INT NULL,
  `comment` VARCHAR(45) NULL,
  `write_time` VARCHAR(45) NULL,
  PRIMARY KEY (`reviewcomment_id`, `review_review_id`, `review_movie_movie_code`),
  CONSTRAINT `fk_review_comment_review1`
    FOREIGN KEY (`review_review_id` , `review_movie_movie_code`)
    REFERENCES `naver_movie`.`review` (`review_id` , `movie_movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_review_comment_review1_idx` ON `naver_movie`.`review_comment` (`review_review_id` ASC, `review_movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`genre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`genre` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`genre` (
  `genre_name` VARCHAR(10) NOT NULL,
  `movie_movie_code` INT NOT NULL,
  PRIMARY KEY (`genre_name`, `movie_movie_code`),
  CONSTRAINT `fk_genre_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_genre_movie1_idx` ON `naver_movie`.`genre` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`country`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`country` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`country` (
  `country_code` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`country_code`, `movie_movie_code`),
  CONSTRAINT `fk_country_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_country_movie1_idx` ON `naver_movie`.`country` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`company` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`company` (
  `company_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`company_id`, `movie_movie_code`),
  CONSTRAINT `fk_company_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_company_movie1_idx` ON `naver_movie`.`company` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`photo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`photo` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`photo` (
  `photo_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `url` VARCHAR(45) NULL,
  PRIMARY KEY (`photo_id`, `movie_movie_code`),
  CONSTRAINT `fk_photo_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_photo_movie1_idx` ON `naver_movie`.`photo` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`video`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`video` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`video` (
  `video_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `video_url` VARCHAR(300) NULL,
  `thumbnail_url` VARCHAR(300) NULL,
  `title` VARCHAR(45) NULL,
  PRIMARY KEY (`video_id`, `movie_movie_code`),
  CONSTRAINT `fk_video_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_video_movie1_idx` ON `naver_movie`.`video` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`enjoy_point`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`enjoy_point` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`enjoy_point` (
  `enjoy_point_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `production` VARCHAR(45) NULL,
  `acting` VARCHAR(45) NULL,
  `story` VARCHAR(45) NULL,
  `recording_beauty` VARCHAR(45) NULL,
  `ost` VARCHAR(45) NULL,
  PRIMARY KEY (`enjoy_point_id`, `movie_movie_code`),
  CONSTRAINT `fk_enjoy_point_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_enjoy_point_movie1_idx` ON `naver_movie`.`enjoy_point` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`satisfying_netizen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`satisfying_netizen` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`satisfying_netizen` (
  `satisfying_netizen_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `male` DOUBLE NULL,
  `female` DOUBLE NULL,
  `tenth` DOUBLE NULL,
  `twentieth` DOUBLE NULL,
  `thirtieth` DOUBLE NULL,
  `fortieth` DOUBLE NULL,
  `fiftieth` DOUBLE NULL,
  `statistics_comment` VARCHAR(300) NULL,
  PRIMARY KEY (`satisfying_netizen_id`, `movie_movie_code`),
  CONSTRAINT `fk_satisfying_netizen_movie1`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_satisfying_netizen_movie1_idx` ON `naver_movie`.`satisfying_netizen` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`viewing_trend`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`viewing_trend` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`viewing_trend` (
  `viewing_trend_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `male` INT NULL,
  `female` INT NULL,
  `tenth` INT NULL,
  `twentieth` INT NULL,
  `thirtieth` INT NULL,
  `fortieth` INT NULL,
  `fiftieth` INT NULL,
  PRIMARY KEY (`viewing_trend_id`, `movie_movie_code`),
  CONSTRAINT `fk_satisfying_netizen_movie10`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_satisfying_netizen_movie1_idx` ON `naver_movie`.`viewing_trend` (`movie_movie_code` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `naver_movie`.`satisfying_viewer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `naver_movie`.`satisfying_viewer` ;

CREATE TABLE IF NOT EXISTS `naver_movie`.`satisfying_viewer` (
  `satisfying_viewer_id` INT NOT NULL AUTO_INCREMENT,
  `movie_movie_code` INT NOT NULL,
  `male` DOUBLE NULL,
  `female` DOUBLE NULL,
  `tenth` DOUBLE NULL,
  `twentieth` DOUBLE NULL,
  `thirtieth` DOUBLE NULL,
  `fortieth` DOUBLE NULL,
  `fiftieth` DOUBLE NULL,
  `statistics_comment` VARCHAR(300) NULL,
  PRIMARY KEY (`satisfying_viewer_id`, `movie_movie_code`),
  CONSTRAINT `fk_satisfying_netizen_movie100`
    FOREIGN KEY (`movie_movie_code`)
    REFERENCES `naver_movie`.`movie` (`movie_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_satisfying_netizen_movie1_idx` ON `naver_movie`.`satisfying_viewer` (`movie_movie_code` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
