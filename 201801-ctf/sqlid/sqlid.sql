-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2017-05-08 09:01:33
-- 服务器版本： 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sqlid`
--
CREATE DATABASE IF NOT EXISTS `sqlid` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `sqlid`;

-- --------------------------------------------------------

--
-- 表的结构 `admin`
--
-- 创建时间： 2017-05-08 06:42:14
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` mediumtext COLLATE utf8_bin NOT NULL,
  `password` mediumtext COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', '8211d7b4ba2828919651');

-- --------------------------------------------------------

--
-- 表的结构 `hint`
--
-- 创建时间： 2017-05-08 06:43:00
--

CREATE TABLE `hint` (
  `id` mediumtext COLLATE utf8_bin NOT NULL,
  `hint` mediumtext COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `hint`
--

INSERT INTO `hint` (`id`, `hint`) VALUES
('1', 'there is no hint');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

CREATE USER 'rebirth'@'localhost' IDENTIFIED BY 'root_1234';
GRANT SELECT ON `sqlid`.* TO 'rebirth'@'localhost' IDENTIFIED BY 'root_1234';
