
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tradingbot
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tradingbot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `tradingbot` ;


-- -----------------------------------------------------
-- Table `tradingbot`.`operations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tradingbot`.`operations` (
  `date` VARCHAR(100) NOT NULL,
  `market` VARCHAR(100) NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  `result` TINYINT(1) NOT NULL,
  `ammount_use` DECIMAL NOT NULL,
  `profit` INT DECIMAL NOT NULL,
  `duration_in_sec` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;