/*
  Warnings:

  - You are about to drop the `Recipient` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Sender` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `email_attachment` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `email_message` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Recipient" DROP CONSTRAINT "Recipient_message_id_fkey";

-- DropForeignKey
ALTER TABLE "Sender" DROP CONSTRAINT "Sender_message_id_fkey";

-- DropForeignKey
ALTER TABLE "email_attachment" DROP CONSTRAINT "email_attachment_message_id_fkey";

-- DropForeignKey
ALTER TABLE "email_attachment" DROP CONSTRAINT "email_attachment_nylas_account_id_fkey";

-- DropForeignKey
ALTER TABLE "email_message" DROP CONSTRAINT "email_message_nylas_accountId_fkey";

-- AlterTable
ALTER TABLE "nylas_account" ADD COLUMN     "deleted_at" TIMESTAMP(3),
ADD COLUMN     "expired" BOOLEAN NOT NULL DEFAULT false;

-- DropTable
DROP TABLE "Recipient";

-- DropTable
DROP TABLE "Sender";

-- DropTable
DROP TABLE "email_attachment";

-- DropTable
DROP TABLE "email_message";
