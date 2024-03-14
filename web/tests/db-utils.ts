import fs from 'node:fs'
import { faker } from '@faker-js/faker'
import { type PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'
import { UniqueEnforcer } from 'enforce-unique'

const uniqueUsernameEnforcer = new UniqueEnforcer()

export function createUser() {
	const firstName = faker.person.firstName()
	const lastName = faker.person.lastName()

	const username = uniqueUsernameEnforcer
		.enforce(() => {
			return (
				faker.string.alphanumeric({ length: 2 }) +
				'_' +
				faker.internet.userName({
					firstName: firstName.toLowerCase(),
					lastName: lastName.toLowerCase(),
				})
			)
		})
		.slice(0, 20)
		.toLowerCase()
		.replace(/[^a-z0-9_]/g, '_')
	return {
		username,
		name: `${firstName} ${lastName}`,
		email: `${username}@example.com`,
	}
}

export function createPassword(password: string = faker.internet.password()) {
	return {
		hash: bcrypt.hashSync(password, 10),
	}
}

let noteImages: Array<Awaited<ReturnType<typeof img>>> | undefined
export async function getNoteImages() {
	if (noteImages) return noteImages

	noteImages = await Promise.all([
		img({
			alt_text: 'a nice country house',
			filepath: './tests/fixtures/images/notes/0.png',
		}),
		img({
			alt_text: 'a city scape',
			filepath: './tests/fixtures/images/notes/1.png',
		}),
		img({
			alt_text: 'a sunrise',
			filepath: './tests/fixtures/images/notes/2.png',
		}),
		img({
			alt_text: 'a group of friends',
			filepath: './tests/fixtures/images/notes/3.png',
		}),
		img({
			alt_text: 'friends being inclusive of someone who looks lonely',
			filepath: './tests/fixtures/images/notes/4.png',
		}),
		img({
			alt_text: 'an illustration of a hot air balloon',
			filepath: './tests/fixtures/images/notes/5.png',
		}),
		img({
			alt_text:
				'an office full of laptops and other office equipment that look like it was abandoned in a rush out of the building in an emergency years ago.',
			filepath: './tests/fixtures/images/notes/6.png',
		}),
		img({
			alt_text: 'a rusty lock',
			filepath: './tests/fixtures/images/notes/7.png',
		}),
		img({
			alt_text: 'something very happy in nature',
			filepath: './tests/fixtures/images/notes/8.png',
		}),
		img({
			alt_text: `someone at the end of a cry session who's starting to feel a little better.`,
			filepath: './tests/fixtures/images/notes/9.png',
		}),
	])

	return noteImages
}

let userImages: Array<Awaited<ReturnType<typeof img>>> | undefined
export async function getUserImages() {
	if (userImages) return userImages

	userImages = await Promise.all(
		Array.from({ length: 10 }, (_, index) =>
			img({ filepath: `./tests/fixtures/images/user/${index}.jpg` }),
		),
	)

	return userImages
}

export async function img({
	alt_text,
	filepath,
}: {
	alt_text?: string
	filepath: string
}) {
	return {
		alt_text,
		content_type: filepath.endsWith('.png') ? 'image/png' : 'image/jpeg',
		blob: await fs.promises.readFile(filepath),
	}
}

export async function cleanupDb(prisma: PrismaClient) {
	// sqllite version
	// const tables = await prisma.$queryRaw<
	// 	{ name: string }[]
	// >`SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_prisma_migrations';`

	// await prisma.$transaction([
	// 	// Disable FK constraints to avoid relation conflicts during deletion
	// 	prisma.$executeRawUnsafe(`PRAGMA foreign_keys = OFF`),
	// 	// Delete all rows from each table, preserving table structures
	// 	...tables.map(({ name }) =>
	// 		prisma.$executeRawUnsafe(`DELETE from "${name}"`),
	// 	),
	// 	prisma.$executeRawUnsafe(`PRAGMA foreign_keys = ON`),
	// ])

	// postgres version
	type Table = { tablename: string }
	const tables = await prisma.$queryRaw<
		Table[]
	>`SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE '_prisma_migrations';`

	await prisma.$transaction([
		prisma.$executeRawUnsafe(
			`TRUNCATE TABLE ${tables.map((t: Table) => `"${t.tablename}"`).join(', ')} RESTART IDENTITY CASCADE;`,
		),
	])
}
