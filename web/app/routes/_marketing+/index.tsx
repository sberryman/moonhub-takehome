import { type MetaFunction } from '@remix-run/node'
import {
	Tooltip,
	TooltipContent,
	TooltipProvider,
	TooltipTrigger,
} from '#app/components/ui/tooltip.tsx'
import { cn } from '#app/utils/misc.tsx'
import { logos } from './logos/logos.ts'
import { MoonhubLogo } from '#app/components/logo.tsx'

export const meta: MetaFunction = () => [{ title: 'Moonhub Takehome' }]

// Tailwind Grid cell classes lookup
const columnClasses: Record<(typeof logos)[number]['column'], string> = {
	1: 'xl:col-start-1',
	2: 'xl:col-start-2',
	3: 'xl:col-start-3',
	4: 'xl:col-start-4',
	5: 'xl:col-start-5',
}
const rowClasses: Record<(typeof logos)[number]['row'], string> = {
	1: 'xl:row-start-1',
	2: 'xl:row-start-2',
	3: 'xl:row-start-3',
	4: 'xl:row-start-4',
	5: 'xl:row-start-5',
	6: 'xl:row-start-6',
}

export default function Index() {
	return (
		<main className="font-poppins grid h-full place-items-center">
			<div className="grid place-items-center px-4 py-16 xl:grid-cols-2 xl:gap-24">
				<div className="flex max-w-md flex-col items-center text-center xl:order-2 xl:items-start xl:text-left">
					<a
						href="https://www.moonhub.ai"
						className="animate-slide-top [animation-fill-mode:backwards] xl:animate-slide-left xl:[animation-delay:0.5s] xl:[animation-fill-mode:backwards]"
					>
						{/* <img
							src="/img/logo.svg"
							alt="Moonhub"
							className="h-14 text-white dark:text-white"
						/> */}
						<MoonhubLogo className="h-14 text-black dark:text-white" />
					</a>
					<h1
						data-heading
						className="mt-8 animate-slide-top text-4xl font-medium text-foreground [animation-fill-mode:backwards] [animation-delay:0.3s] md:text-5xl xl:mt-4 xl:animate-slide-left xl:text-6xl xl:[animation-fill-mode:backwards] xl:[animation-delay:0.8s]"
					>
						{/* <a href="https://www.moonhub.ai">Hire exceptional talent beyond your network</a> */}
						Fullstack Take-home
					</h1>
					<p
						data-paragraph
						className="mt-6 animate-slide-top text-xl/7 text-muted-foreground [animation-fill-mode:backwards] [animation-delay:0.8s] xl:mt-8 xl:animate-slide-left xl:text-xl/6 xl:leading-10 xl:[animation-fill-mode:backwards] xl:[animation-delay:1s]"
					>
						Log In using the credentials provided to you to see a demo of the
						take-home.
					</p>
				</div>
				<ul className="mt-8 flex max-w-3xl flex-wrap justify-center pr-16">
					<img
						src="https://assets-global.website-files.com/64edb586d45ab1cdd8f43d85/65ee9e70ff06a331aa6dd408_Moonhub%20Hero%20image%20updated-min.png"
						alt="Moonhub"
						className="w-11/12 text-black dark:text-white"
					/>
				</ul>
			</div>
		</main>
	)
}
