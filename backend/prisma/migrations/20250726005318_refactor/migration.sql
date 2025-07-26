/*
  Warnings:

  - You are about to drop the `Alert` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Configuration` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Device` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Notification` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `RefreshToken` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `SensorReading` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE `Alert` DROP FOREIGN KEY `Alert_deviceId_fkey`;

-- DropForeignKey
ALTER TABLE `Configuration` DROP FOREIGN KEY `Configuration_userId_fkey`;

-- DropForeignKey
ALTER TABLE `Device` DROP FOREIGN KEY `Device_ownerId_fkey`;

-- DropForeignKey
ALTER TABLE `Notification` DROP FOREIGN KEY `Notification_userId_fkey`;

-- DropForeignKey
ALTER TABLE `RefreshToken` DROP FOREIGN KEY `RefreshToken_userID_fkey`;

-- DropForeignKey
ALTER TABLE `SensorReading` DROP FOREIGN KEY `SensorReading_deviceId_fkey`;

-- DropTable
DROP TABLE `Alert`;

-- DropTable
DROP TABLE `Configuration`;

-- DropTable
DROP TABLE `Device`;

-- DropTable
DROP TABLE `Notification`;

-- DropTable
DROP TABLE `RefreshToken`;

-- DropTable
DROP TABLE `SensorReading`;

-- DropTable
DROP TABLE `User`;

-- CreateTable
CREATE TABLE `DeseaseDectection` (
    `deviceId` VARCHAR(191) NOT NULL,
    `timestamp` DATETIME(3) NOT NULL,
    `disease` VARCHAR(191) NOT NULL,
    `confidence` DOUBLE NOT NULL,

    PRIMARY KEY (`deviceId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
