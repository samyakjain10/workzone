-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2020 at 10:21 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ishaan kamra`
--

-- --------------------------------------------------------

--
-- Table structure for table `branches`
--

CREATE TABLE `branches` (
  `Sno` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Head` text NOT NULL,
  `Address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `branches`
--

INSERT INTO `branches` (`Sno`, `Name`, `Head`, `Address`) VALUES
(1, 'Delhi', 'Branch Head 1', 'New Delhi'),
(2, 'Mumbai', 'Branch Head 2', 'Andheri'),
(4, 'Bangalore', ' ', 'Bangalore');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `image` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`sno`, `name`, `image`) VALUES
(9, 'Influential Marketing', 'Influencer-Marketing.jpg'),
(10, 'Web development', 'web-development.jpg'),
(11, 'App Development', 'App-Development.png'),
(12, 'Network Marketing', 'network_marketing.jpg'),
(13, 'Digital Marketing', 'DIGITAL-MARKETING.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Phone` varchar(12) NOT NULL,
  `Password` text NOT NULL,
  `Branch` text DEFAULT NULL,
  `Department` text NOT NULL,
  `Designation` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`id`, `Name`, `Email`, `Phone`, `Password`, `Branch`, `Department`, `Designation`) VALUES
(1, 'Founder 1', 'founder1@gmail.com', '9876543210', 'pbkdf2:sha256:150000$gfxf4S5g$0b5580e2c082ab9977e58b8dc214da003fd0221b3c1a535dc861f06a169631e8', 'Delhi', 'Influential Marketing', 'Founder'),
(31, 'Founder 2', 'founder2@gmail.com', '9876543210', 'sha256$R0WBTJ9y$10995a173bfde8241d51c4c7c33ae818a6b685768ed9cbad9fd4696d7d4b5f9f', 'Mumbai', 'Influential Marketing', 'Founder'),
(32, 'Branch Head 1', 'bh1@gmail.com', '9876543210', 'sha256$aXkT54ew$fa860611b1861c0093cd8a68b6128d7b6840fc73d9d6f7120d22125dd954bf58', 'Delhi', 'Influential Marketing', 'Branch Head'),
(33, 'Branch Head 2', 'bh2@gmail.com', '9876543210', 'sha256$2DtWRVqb$98664a97475448763d439f419881bd1e8564b8796917df4b95c690a5eefe10de', 'Mumbai', 'Digital Marketing', 'Branch Head'),
(34, 'Employee 1', 'employee1@gmail.com', '9876543210', 'sha256$QuNb8Y9c$b3852e4a74a45690e0c41fc641d1d21d64efaf3a66dd298b4fe680a9ba40e247', 'Delhi', 'Web development', 'Employee'),
(35, 'Employee 2', 'employee2@gmail.com', '9876543210', 'sha256$VOzfQcKl$31330963d7a9cb5eb3e308f5ba069f44f2f16da2f85d8137466a55995bde751b', 'Delhi', 'Network Marketing', 'Employee'),
(36, 'Employee 3', 'employee3@gmail.com', '9876543210', 'sha256$uoo9zcEu$47d4abf1f2da506dc66c76866a6af0eb2c97c97aa6c4755c0e0de535d89eebed', 'Mumbai', 'Influential Marketing', 'Employee'),
(37, 'Employee 4', 'employee4@gmail.com', '9876543210', 'sha256$NxQJuS0M$a9ff5323d4d6444b13ad1bd1aceb103ed753a2e6f7fcd12f877fbc455b0b23fc', 'Mumbai', 'App Development', 'Employee');

-- --------------------------------------------------------

--
-- Table structure for table `new`
--

CREATE TABLE `new` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone_no` int(100) NOT NULL,
  `branch` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `department` text NOT NULL,
  `employee` mediumtext NOT NULL,
  `branch` varchar(100) NOT NULL,
  `date` date DEFAULT current_timestamp(),
  `status` text NOT NULL,
  `description` text NOT NULL,
  `report` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`sno`, `name`, `department`, `employee`, `branch`, `date`, `status`, `description`, `report`) VALUES
(11, 'Project 1', 'Influential Marketing', '[\"founder1@gmail.com\", \"employee1@gmail.com\"]', 'Delhi', '2020-04-24', 'ACTIVE', 'This is a test description', '[]'),
(12, 'Project 2', 'Influential Marketing', '[\"bh1@gmail.com\"]', 'Mumbai', '2020-04-24', 'COMPLETED', 'This is a test description', '[]'),
(13, 'Project 3', 'Web development', '[\"bh2@gmail.com\"]', 'Delhi', '2020-04-24', 'ACTIVE', 'This is a test description', '[]'),
(14, 'Project 4', 'App Development', '[\"bh1@gmail.com\"]', 'Mumbai', '2020-04-24', 'COMPLETED', 'This is a test description', '[]'),
(15, 'Project 5', 'Network Marketing', '[\"bh2@gmail.com\"]', 'Delhi', '2020-04-24', 'ACTIVE', 'This is a test description', '[]');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `branches`
--
ALTER TABLE `branches`
  ADD PRIMARY KEY (`Sno`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `new`
--
ALTER TABLE `new`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `branches`
--
ALTER TABLE `branches`
  MODIFY `Sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `new`
--
ALTER TABLE `new`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
