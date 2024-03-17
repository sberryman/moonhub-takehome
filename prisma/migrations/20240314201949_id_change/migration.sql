/*
  Warnings:

  - The primary key for the `Recipient` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `Sender` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `email_attachment` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "Recipient" DROP CONSTRAINT "Recipient_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "Recipient_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Recipient_id_seq";

-- AlterTable
ALTER TABLE "Sender" DROP CONSTRAINT "Sender_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "Sender_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Sender_id_seq";

-- AlterTable
ALTER TABLE "email_attachment" DROP CONSTRAINT "email_attachment_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "email_attachment_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "email_attachment_id_seq";
