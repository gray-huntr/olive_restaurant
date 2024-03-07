-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 18, 2023 at 11:49 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `olive_garden`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` int(15) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`first_name`, `last_name`, `email`, `number`, `password`) VALUES
('Lennox', 'Kulecho', 'lenox@gmail.com', 751123478, '1234');

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `first_name` varchar(15) NOT NULL,
  `last_name` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` int(15) NOT NULL,
  `location` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`first_name`, `last_name`, `email`, `number`, `location`, `password`) VALUES
('Lennox', 'Kulecho', 'lenox@gmail.com', 111368315, 'gachie', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `device`
--

CREATE TABLE `device` (
  `uid` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'open'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `device`
--

INSERT INTO `device` (`uid`, `status`) VALUES
('D101', 'assigned'),
('D102', 'open'),
('D103', 'assigned'),
('D104', 'open');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` varchar(6) NOT NULL,
  `first_name` varchar(15) NOT NULL,
  `last_name` varchar(15) NOT NULL,
  `number` int(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `category` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `first_name`, `last_name`, `number`, `email`, `category`) VALUES
('W001', 'Faith', 'Kari', 712345678, 'fkariuki@gmail.com', 'Rider'),
('W002', 'Janice', 'Luchiva', 711345231, 'jluchiva@gmail.com', 'Service_staff'),
('W003', 'David', 'Kim', 712345678, 'Kimani@gmail.com', 'Kitchen_staff'),
('W004', 'Emmanuel', 'kiprotich', 712345876, 'emmanuel@gmail.com', 'Rider'),
('W005', 'Julius', 'Ceasar', 789543267, 'jceaser@gmail.com', 'Service_staff');

-- --------------------------------------------------------

--
-- Table structure for table `inhouse_orders`
--

CREATE TABLE `inhouse_orders` (
  `auto_number` int(11) NOT NULL,
  `order_id` varchar(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `status` varchar(15) NOT NULL DEFAULT 'In preparation',
  `Device_uid` varchar(10) NOT NULL,
  `Table_number` varchar(10) NOT NULL,
  `cost` int(10) NOT NULL,
  `Quantity` int(10) NOT NULL,
  `Total` int(10) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL DEFAULT current_timestamp(),
  `served_by` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inhouse_orders`
--

INSERT INTO `inhouse_orders` (`auto_number`, `order_id`, `name`, `status`, `Device_uid`, `Table_number`, `cost`, `Quantity`, `Total`, `date`, `time`, `served_by`) VALUES
(1, 'J1001V', 'Full chicken', 'Complete', 'D101', 't106', 600, 6, 3600, '2023-10-07', '01:16:30', 'W002Janice'),
(2, 'J1001V', '1/4 chicken', 'Complete', 'D101', 't106', 150, 2, 300, '2023-10-07', '01:16:30', 'W002Janice'),
(3, 'J1002V', 'Fried fish', 'Complete', 'D101', 't106', 450, 1, 450, '2023-10-07', '01:16:30', 'W002Janice'),
(4, 'J1003V', 'Chips masala', 'On its way', 'D101', 't106', 150, 1, 150, '2023-10-07', '01:16:30', NULL),
(5, 'J1004V', '1/4 chicken', 'On its way', 'D101', 't106', 150, 1, 150, '2023-10-07', '01:16:30', NULL),
(6, 'J1004V', 'Chips', 'On its way', 'D101', 't106', 100, 1, 100, '2023-10-07', '01:16:30', NULL),
(7, 'J1007V', 'Black current (300 M', 'On its way', 'D101', 'T102', 60, 1, 60, '2023-10-07', '15:47:05', NULL),
(8, 'J1007V', 'Stoney (500 ML)', 'On its way', 'D101', 'T102', 100, 4, 400, '2023-10-07', '15:47:05', NULL),
(9, 'J1007V', 'Coca cola (500 ML)', 'On its way', 'D101', 'T102', 100, 1, 100, '2023-10-07', '15:47:05', NULL),
(10, 'J1008V', 'Chips', 'On its way', 'D101', 'T102', 100, 1, 100, '2023-10-07', '21:55:43', NULL),
(11, 'J1008V', 'Sausage', 'On its way', 'D101', 'T102', 60, 1, 60, '2023-10-07', '21:55:43', NULL),
(12, 'J1008V', '1/4 chicken', 'On its way', 'D101', 'T102', 150, 1, 150, '2023-10-07', '21:55:43', NULL),
(13, 'J1008V', 'Coca cola (300 ML)', 'On its way', 'D101', 'T102', 60, 1, 60, '2023-10-07', '21:55:43', NULL),
(14, 'J1025V', 'Sausage', 'In preparation', 'D101', 'T102', 60, 1, 60, '2023-10-14', '16:09:19', NULL),
(15, 'J1025V', 'Chips', 'In preparation', 'D101', 'T102', 100, 1, 100, '2023-10-14', '16:09:19', NULL),
(16, 'J1025V', '1/4 chicken', 'In preparation', 'D101', 'T102', 150, 1, 150, '2023-10-14', '16:09:19', NULL),
(17, 'J1025V', 'Black current (300 M', 'In preparation', 'D101', 'T102', 60, 1, 60, '2023-10-14', '16:09:19', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `picture` varchar(20) NOT NULL,
  `Description` varchar(1000) NOT NULL,
  `price` int(5) NOT NULL,
  `category` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id`, `name`, `picture`, `Description`, `price`, `category`) VALUES
(1, 'Chips', 'chips.jpg', 'A bowl of deliciously salted hot chips that have just the right amount of crispiness', 100, 'Food'),
(2, 'Full chicken', 'chicken.jpg', 'This rotisserie chicken recipe is perfectly juicy and moist.', 600, 'Food'),
(3, '1/2 chicken', 'half_chicken.jpeg', 'Well cooked half chicken', 300, 'Food'),
(4, '1/4 chicken', 'quarter_chicken.jpg', 'Well cooked quarter chicken', 150, 'Food'),
(5, 'Chicken wings', 'chicken_wings.jpg', 'Chicken wings dipped in honey', 70, 'Food'),
(6, 'Bhajia', 'bhajia.png', 'Deep fried potatoe slices', 120, 'Food'),
(7, 'Chips masala', 'chips_masala.jpg', 'T﻿hese delicious spicy masala chips or fries are a wonderful quick and easy side dish or snack ', 150, 'Food'),
(8, 'Fried fish', 'fish.jpg', 'wet/dry fry fish with a side of ugali and kales', 450, 'Food'),
(9, 'Beef pilau', 'pilau.jpg', 'Tasty beef pilau', 150, 'Food'),
(10, 'Soda', 'soda.jpg', 'A variety of sodas to choose from, pick yours below', 60, 'Drinks'),
(11, 'Fresh juice', 'fresh_juice.jpg', 'A variety of drinks to choose from, pick your choice below', 60, 'Drinks'),
(12, 'Youghurt', 'youghurt.jpg', 'Youghurt smoothie', 60, 'Drinks'),
(13, 'Sausage', 'sausage.jpg', 'If you love sausages, then this is the place for you', 60, 'Appetizer'),
(14, 'Meat Samosa', 'samosa.jpg', 'Enjoy a tasty meat samosa ', 50, 'Appetizer'),
(15, 'Kebab', 'kebab.jpg', 'Enjoy a tasty Kebab ', 80, 'Appetizer'),
(16, 'Shawarma', 'shawarma.jpg', 'Enjoy a tasty appetizer', 200, 'Appetizer'),
(17, 'Sausage rolls', 'sausage_rolls.jpeg', 'Enjoy a tasty sausage roll', 60, 'Appetizer'),
(18, 'Chicken pie', 'chicken_pie.jpg', 'Enjoy a tasty chicken pie', 120, 'Appetizer'),
(19, 'Meat pie', 'meat_pie.jpg', 'Enjoy a tasty meat pie', 120, 'Appetizer');

-- --------------------------------------------------------

--
-- Table structure for table `tables`
--

CREATE TABLE `tables` (
  `table_id` varchar(11) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'open'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tables`
--

INSERT INTO `tables` (`table_id`, `status`) VALUES
('T101', 'open'),
('T102', 'in use'),
('T103', 'open'),
('T104', 'open'),
('T105', 'open'),
('T106', 'open');

-- --------------------------------------------------------

--
-- Table structure for table `table_assignments`
--

CREATE TABLE `table_assignments` (
  `id` int(11) NOT NULL,
  `assignee_id` varchar(20) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `Device_uid` varchar(10) NOT NULL,
  `table_id` varchar(10) NOT NULL,
  `Date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `table_assignments`
--

INSERT INTO `table_assignments` (`id`, `assignee_id`, `first_name`, `last_name`, `Device_uid`, `table_id`, `Date`, `time`) VALUES
(1, 'W001', '0', '0', 'D101', 'T102', '2023-10-06', '16:41:04'),
(2, 'W001', 'Faith', 'Kariuki', 'D101', 'T102', '2023-10-06', '16:45:17'),
(3, 'w002', 'Janice', 'Luchiva', 'd103', 't106', '2023-10-06', '16:55:44'),
(4, 'W001', 'Faith', 'Kariuki', 'D101', 't106', '2023-10-07', '00:09:13'),
(5, 'w002', 'Janice', 'Luchiva', 'D101', 'T102', '2023-10-07', '01:24:50'),
(6, 'W001', 'Faith', 'Kariuki', 'D101', 'T102', '2023-10-07', '15:29:42'),
(7, 'W001', 'Faith', 'Kariuki', 'D101', 'T102', '2023-10-07', '15:31:46'),
(8, 'W001', 'Faith', 'Kariuki', 'D101', 'T102', '2023-10-10', '13:20:08'),
(9, 'W001', 'Faith', 'Kari', 'D101', 'T102', '2023-10-14', '16:06:34');

-- --------------------------------------------------------

--
-- Table structure for table `takeaway_orders`
--

CREATE TABLE `takeaway_orders` (
  `auto_number` int(11) NOT NULL,
  `order_id` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL DEFAULT 'in preparation',
  `ordered_by` varchar(20) NOT NULL,
  `number` int(15) NOT NULL,
  `cost` int(10) NOT NULL,
  `quantity` int(10) NOT NULL,
  `total` int(15) NOT NULL,
  `Delivery_person` varchar(20) DEFAULT NULL,
  `delivery_location` varchar(100) NOT NULL,
  `email` varchar(20) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `takeaway_orders`
--

INSERT INTO `takeaway_orders` (`auto_number`, `order_id`, `name`, `status`, `ordered_by`, `number`, `cost`, `quantity`, `total`, `Delivery_person`, `delivery_location`, `email`, `date`, `time`) VALUES
(1, 'J1022V', 'Coca cola (300 ', 'On its way', 'Lennox', 233313, 60, 1, 60, 'W001Faith', 'gachie', 'lenox@gmail.com', '2023-10-11', '15:01:10'),
(3, 'J1024V', 'Chips', 'On its way', 'Lennox', 233313, 100, 1, 100, 'W004Emmanuel', 'gachie', 'lenox@gmail.com', '2023-10-11', '15:01:10'),
(4, 'J1024V', 'Chicken wings', 'On its way', 'Lennox', 233313, 70, 1, 70, 'W004Emmanuel', 'gachie', 'lenox@gmail.com', '2023-10-11', '15:01:10'),
(5, 'J1024V', 'Chips masala', 'On its way', 'Lennox', 233313, 150, 1, 150, 'W004Emmanuel', 'gachie', 'lenox@gmail.com', '2023-10-11', '15:01:10');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `mpesa_code` int(11) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `Date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `inhouse_orders`
--
ALTER TABLE `inhouse_orders`
  ADD PRIMARY KEY (`auto_number`),
  ADD KEY `employee_id` (`served_by`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tables`
--
ALTER TABLE `tables`
  ADD PRIMARY KEY (`table_id`);

--
-- Indexes for table `table_assignments`
--
ALTER TABLE `table_assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `assignee` (`assignee_id`),
  ADD KEY `table` (`table_id`),
  ADD KEY `device` (`Device_uid`);

--
-- Indexes for table `takeaway_orders`
--
ALTER TABLE `takeaway_orders`
  ADD PRIMARY KEY (`auto_number`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inhouse_orders`
--
ALTER TABLE `inhouse_orders`
  MODIFY `auto_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `table_assignments`
--
ALTER TABLE `table_assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `takeaway_orders`
--
ALTER TABLE `takeaway_orders`
  MODIFY `auto_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `table_assignments`
--
ALTER TABLE `table_assignments`
  ADD CONSTRAINT `assignee` FOREIGN KEY (`assignee_id`) REFERENCES `employees` (`employee_id`),
  ADD CONSTRAINT `device` FOREIGN KEY (`Device_uid`) REFERENCES `device` (`uid`),
  ADD CONSTRAINT `table` FOREIGN KEY (`table_id`) REFERENCES `tables` (`table_id`);

--
-- Constraints for table `takeaway_orders`
--
ALTER TABLE `takeaway_orders`
  ADD CONSTRAINT `email` FOREIGN KEY (`email`) REFERENCES `clients` (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
