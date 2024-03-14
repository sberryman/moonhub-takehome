import { ArrowUpOnSquareIcon } from '@heroicons/react/24/outline'
import { type MetaFunction } from '@remix-run/node'

import { MoonhubIcon } from '#app/components/logo'
import { useHints } from '#app/utils/client-hints'
import { getUserImgSrc } from '#app/utils/misc'
import { useUser } from '#app/utils/user'

export const meta: MetaFunction = () => [
	{ title: 'Projects | Moonhub Takehome' },
]

export default function ProjectsIndex() {
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
			<div className="flex flex-1 flex-col gap-y-5 rounded-lg bg-white dark:bg-gray-900 px-5 py-4">
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
										<div className="flex flex-none flex-row gap-x-2 items-center">
											<div className="font-semibold">
                                                {message.role === "assistant" ? "moonhub" : "you"}
                                            </div>
											<div className="text-gray-500 dark:text-gray-600 dark:text-gray-400 text-sm font-light">
												{dtf.format(Date.parse(message.timestamp))}
											</div>
										</div>
										<div className="flex flex-none pt-1 font-light">{message.content}</div>
									</div>
								</div>
							</li>
						))}
					</ul>
				</div>

				<div className="flex flex-none flex-row gap-x-5 border-t border-gray-300 dark:border-gray-700 pt-4">
					<input
						type="text"
						className="flex flex-grow rounded-md border border-gray-300 dark:border-gray-500 bg-transparent px-4 py-1 focus:stroke-green-500"
						placeholder="Type your message here"
					/>
					<button
						type="button"
						className="flex flex-none rounded-md border border-gray-300 dark:border-gray-500 px-4 py-1 hover:text-blue-300"
					>
						Send
					</button>
				</div>
			</div>
			<div className="flex flex-1 flex-col gap-y-5 rounded-lg bg-white dark:bg-gray-900 px-5 py-4">
				{/* header */}
				<div className="flex flex-none flex-row justify-center gap-y-2">
					<div className="flex-grow text-xl font-light">Unread Emails</div>
				</div>

				<div className="flex flex-1 flex-col justify-center rounded-lg border border-dashed border-gray-300 dark:border-gray-500 px-5 py-4 text-center">
					<div className="flex flex-grow" />
					<div className="flex flex-none justify-center text-gray-600 dark:text-gray-400">
						List of unread emails will be displayed here
					</div>
					<div className="flex flex-grow" />
				</div>
			</div>
		</div>
	)
}
