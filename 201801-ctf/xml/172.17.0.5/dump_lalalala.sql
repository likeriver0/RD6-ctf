
USE `flag`;

DROP TABLE IF EXISTS `flag`;
CREATE TABLE `flag` (
  `flag` VARCHAR(100)
);

CREATE USER 'rebirth'@'localhost';
GRANT USAGE ON *.* TO 'rebirth'@'localhost';
GRANT SELECT ON `flag`.* TO 'rebirth'@'localhost';
