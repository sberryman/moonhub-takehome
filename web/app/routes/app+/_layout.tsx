import { invariantResponse } from '@epic-web/invariant'
import { Dialog, Transition } from '@headlessui/react'
import {
	Bars3Icon,
	FolderIcon,
	HomeIcon,
	XMarkIcon,
} from '@heroicons/react/24/outline'
import { json, type LoaderFunctionArgs } from '@remix-run/node'
import { Link, Outlet, useLoaderData, useLocation } from '@remix-run/react'
import { Fragment, useState } from 'react'
import { MoonhubIcon } from '#app/components/logo.tsx'
import { EpicProgress } from '#app/components/progress-bar.tsx'
import { useToast } from '#app/components/toaster.tsx'
import { EpicToaster } from '#app/components/ui/sonner.tsx'
import { useTheme } from '#app/root'
import { requireUserId } from '#app/utils/auth.server.ts'
import { classNames } from '#app/utils/class-names'
import { prisma } from '#app/utils/db.server.ts'
import { combineHeaders } from '#app/utils/misc.tsx'
import { getToast } from '#app/utils/toast.server.ts'

export async function loader({ request }: LoaderFunctionArgs) {
	const userId = await requireUserId(request)
	const user = await prisma.user.findUniqueOrThrow({
		where: { id: userId },
		select: { username: true },
	})
	invariantResponse(user, 'User not found', { status: 404 })

	const { toast, headers: toastHeaders } = await getToast(request)

	return json(
		{
			user,
			toast,
		},
		{
			headers: combineHeaders(toastHeaders),
		},
	)
}

export default function AppLayout() {
	const data = useLoaderData<typeof loader>()
	// const user = useUser()
	const theme = useTheme()
	useToast(data.toast)

	const [sidebarOpen, setSidebarOpen] = useState(false)


	let navigation = [
		{ name: 'Dashboard', href: '/app', icon: HomeIcon, current: true },
		{ name: 'Projects', href: '/app/projects', icon: FolderIcon, current: false },
		// { name: 'Calendar', href: '#', icon: CalendarIcon, current: false },
		// { name: 'Documents', href: '#', icon: DocumentDuplicateIcon, current: false },
		// { name: 'Reports', href: '#', icon: ChartPieIcon, current: false },
	]

    const location = useLocation();
    navigation = navigation.map((item) => {
        item.current = location.pathname.startsWith(item.href);
		return item
    });
    navigation[0].current = location.pathname === navigation[0].href;

	return (
		<>
			<div className="flex h-full flex-1 gap-x-5 px-5 py-4">
				<Transition.Root show={sidebarOpen} as={Fragment}>
					<Dialog
						as="div"
						className="relative z-50 lg:hidden"
						onClose={setSidebarOpen}
					>
						<Transition.Child
							as={Fragment}
							enter="transition-opacity ease-linear duration-300"
							enterFrom="opacity-0"
							enterTo="opacity-100"
							leave="transition-opacity ease-linear duration-300"
							leaveFrom="opacity-100"
							leaveTo="opacity-0"
						>
							<div className="fixed inset-0 bg-gray-900/80" />
						</Transition.Child>

						<div className="fixed inset-0 flex">
							<Transition.Child
								as={Fragment}
								enter="transition ease-in-out duration-300 transform"
								enterFrom="-translate-x-full"
								enterTo="translate-x-0"
								leave="transition ease-in-out duration-300 transform"
								leaveFrom="translate-x-0"
								leaveTo="-translate-x-full"
							>
								<Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
									<Transition.Child
										as={Fragment}
										enter="ease-in-out duration-300"
										enterFrom="opacity-0"
										enterTo="opacity-100"
										leave="ease-in-out duration-300"
										leaveFrom="opacity-100"
										leaveTo="opacity-0"
									>
										<div className="absolute left-full top-0 flex w-16 justify-center pt-5">
											<button
												type="button"
												className="-m-2.5 p-2.5"
												onClick={() => setSidebarOpen(false)}
											>
												<span className="sr-only">Close sidebar</span>
												<XMarkIcon
													className="h-6 w-6 text-white"
													aria-hidden="true"
												/>
											</button>
										</div>
									</Transition.Child>

									<div className="flex grow flex-col gap-y-5 overflow-y-auto bg-gray-900 px-6 pb-2 ring-1 ring-white/10">
										<div className="flex h-16 shrink-0 items-center">
											<MoonhubIcon className="h-8 w-auto" />
										</div>
										<nav className="flex flex-1 flex-col">
											<ul className="-mx-2 flex-1 space-y-1">
												{navigation.map(item => (
													<li key={item.name}>
														<a
															href={item.href}
															className={classNames(
																item.current
																	? 'bg-gray-800 text-white'
																	: 'text-gray-400 hover:bg-gray-800 hover:text-white',
																'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6',
															)}
														>
															<item.icon
																className="h-6 w-6 shrink-0"
																aria-hidden="true"
															/>
															{item.name}
														</a>
													</li>
												))}
											</ul>
										</nav>
									</div>
								</Dialog.Panel>
							</Transition.Child>
						</div>
					</Dialog>
				</Transition.Root>

				{/* Static sidebar for desktop */}
				<div className="flex rounded-lg bg-gray-900 px-1.5 lg:flex-col lg:pb-4">
					<div className="flex h-16 shrink-0 items-center justify-center">
						<MoonhubIcon className="h-8 w-auto" />
					</div>
					<nav className="mt-8">
						<ul className="flex flex-col items-center space-y-1">
							{navigation.map(item => (
								<li key={item.name}>
									<a
										href={item.href}
										className={classNames(
											item.current
												? 'bg-gray-800 text-white'
												: 'text-gray-400 hover:bg-gray-800 hover:text-white',
											'group flex gap-x-3 rounded-md p-3 text-sm font-semibold leading-6',
										)}
									>
										<item.icon
											className="h-6 w-6 shrink-0"
											aria-hidden="true"
										/>
										<span className="sr-only">{item.name}</span>
									</a>
								</li>
							))}
						</ul>
					</nav>
				</div>

				<div className="sticky top-0 z-40 flex items-center gap-x-6 bg-gray-900 px-4 py-4 shadow-sm sm:px-6 lg:hidden">
					<button
						type="button"
						className="-m-2.5 p-2.5 text-gray-400 lg:hidden"
						onClick={() => setSidebarOpen(true)}
					>
						<span className="sr-only">Open sidebar</span>
						<Bars3Icon className="h-6 w-6" aria-hidden="true" />
					</button>
					<div className="flex-1 text-sm font-semibold leading-6 text-white">
						Dashboard
					</div>
					<Link to="#">
						<span className="sr-only">Your profile</span>
						<img
							className="h-8 w-8 rounded-full bg-gray-800"
							src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
							alt=""
						/>
					</Link>
				</div>

				<main className="flex-grow">
					<Outlet />
				</main>
			</div>
			<EpicToaster closeButton position="top-center" theme={theme} />
			<EpicProgress />
		</>
	)
}
