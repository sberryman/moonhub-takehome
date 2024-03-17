import { invariantResponse } from '@epic-web/invariant'
import { ArrowUpOnSquareIcon } from '@heroicons/react/24/outline'
import { type LoaderFunctionArgs, type MetaFunction } from '@remix-run/node'
import { json, useLoaderData } from '@remix-run/react'

import { MoonhubIcon } from '#app/components/logo'
import { useHints } from '#app/utils/client-hints'
import { getUserImgSrc } from '#app/utils/misc'
import { useUser } from '#app/utils/user'
import { apiClient } from '#app/utils/api.server'

export const meta: MetaFunction = () => [
	{ title: 'Projects | Moonhub Takehome' },
]

export async function loader({ params }: LoaderFunctionArgs) {
	const response = await apiClient['/v1/nylas/messages'].get({})
	const messages = await response.json()

	invariantResponse(messages, 'Messages not found', { status: 404 })

	return json({ messages })
}

export default function ProjectsIndex() {
	const data = useLoaderData<typeof loader>()
	const emails = data.messages
	const user = useUser()
	const timeZone = useHints().timeZone
	const dtf = new Intl.DateTimeFormat(undefined, {
		dateStyle: 'medium',
		timeStyle: 'short',
		timeZone,
	})

	const messages = [
		{
			id: 1,
			content: `Good morning ${user.name ?? user.username}! I'd like to remind you that you have 4 meetings today.`,
			role: 'assistant',
			timestamp: '2024-03-14T13:12:35Z',
		},
		{
			id: 2,
			content: `Thanks! Can you please show me all of my unread emails?`,
			role: 'user',
			timestamp: '2024-03-14T13:12:35Z',
		},
		{
			id: 3,
			content: `Of course!`,
			role: 'assistant',
			timestamp: '2024-03-14T13:12:35Z',
		},
		{
			id: 4,
			content: `Here are your unread emails…`,
			role: 'assistant',
			timestamp: '2024-03-14T13:12:35Z',
		},
	]

	return (
		<div className="flex h-full flex-1 gap-x-5">
			<div className="flex flex-1 flex-col gap-y-5 rounded-lg bg-white px-5 py-4 dark:bg-gray-900">
				{/* header */}
				<div className="flex flex-none flex-row justify-center gap-y-2">
					<div className="flex-grow text-xl font-semibold">Senior SWE role</div>
					<div className="flex-none">
						<button type="button" className="hover:text-blue-300">
							<ArrowUpOnSquareIcon className="h-6 w-6" />
						</button>
					</div>
				</div>

				<div className="flex flex-grow">
					<ul className="flex flex-col gap-y-5">
						{messages.map(message => (
							<li key={message.id}>
								<div className="flex flex-row gap-x-4">
									<div className="flex-none pt-1.5">
										{message.role === 'assistant' ? (
											<MoonhubIcon className="h-7 w-7" />
										) : (
											<img
												className="h-7 w-7 rounded-full object-cover"
												alt={user.name ?? user.username}
												src={getUserImgSrc(user.image?.id)}
											/>
										)}
									</div>
									<div className="flex flex-grow flex-col">
										<div className="flex flex-none flex-row items-center gap-x-2">
											<div className="font-semibold">
												{message.role === 'assistant' ? 'moonhub' : 'you'}
											</div>
											<div className="text-sm font-light text-gray-500 dark:text-gray-400">
												{dtf.format(Date.parse(message.timestamp))}
											</div>
										</div>
										<div className="flex flex-none pt-1 font-light">
											{message.content}
										</div>
									</div>
								</div>
							</li>
						))}
					</ul>
				</div>

				<div className="flex flex-none flex-row gap-x-5 border-t border-gray-200 pt-4 dark:border-gray-700">
					<input
						type="text"
						className="flex flex-grow rounded-md border border-gray-300 bg-transparent px-4 py-1 focus:stroke-green-500 dark:border-gray-500"
						placeholder="Type your message here"
					/>
					<button
						type="button"
						className="flex flex-none rounded-md border border-gray-300 px-4 py-1 hover:text-blue-300 dark:border-gray-500"
					>
						Send
					</button>
				</div>
			</div>
			<div className="flex flex-1 flex-col gap-y-5 rounded-lg bg-white px-5 py-4 dark:bg-gray-900  overflow-y-auto">
				{/* header */}
				<div className="flex flex-none flex-row justify-center gap-y-2">
					<div className="flex-grow text-xl font-light">Unread Emails</div>
				</div>

				<div className="flex flex-1 flex-col">
					<ul className="flex flex-col gap-y-5">
						{emails.map((message, index) => {
							const from = message.from?.[0] ?? undefined
							return (
								<li
									key={index}
									className="border-t border-gray-300 dark:border-gray-700 pt-5 first:mt-0 first:border-t-0 first:pt-0"
								>
									<div className="flex flex-row gap-x-4">
										<div className="flex flex-grow flex-col">
											<div className="flex flex-1 flex-row items-center">
												<div className="flex flex-grow font-semibold">
													{from.name ?? from.email ?? "Unknown"}
												</div>
												<div className="flex flex-none text-sm font-light text-gray-500 dark:text-gray-400">
													{message.created_at ? (
														<time
															dateTime={new Date(
																message.created_at * 1000,
															).toISOString()}
														>
															{dtf.format(
																new Date(
																	message.created_at * 1000 || Date.now(),
																),
															)}
														</time>
													) : (
														<span>Unknown</span>
													)}
												</div>
											</div>
											<div className="flex flex-none pt-1 font-light">
												{message.subject}
											</div>
											<div
												className="flex flex-none pt-1 text-sm font-light text-gray-500 dark:text-gray-400"
												dangerouslySetInnerHTML={{
													__html: message.snippet || '',
												}}
											></div>
										</div>
									</div>
								</li>
							)
						})}
					</ul>
				</div>
			</div>
		</div>
	)
}
