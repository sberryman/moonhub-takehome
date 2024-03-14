import { type MetaFunction } from '@remix-run/node'
import { MoonhubLogo } from '#app/components/logo.tsx'

export const meta: MetaFunction = () => [{ title: 'Moonhub Takehome' }]

export default function Index() {
	return (
		<main className="font-poppins grid h-full place-items-center">
			<div className="grid place-items-center px-4 py-16 xl:grid-cols-2 xl:gap-24">
				<div className="flex max-w-md flex-col items-center text-center xl:order-2 xl:items-start xl:text-left">
					<a
						href="https://www.moonhub.ai"
						className="animate-slide-top [animation-fill-mode:backwards] xl:animate-slide-left xl:[animation-delay:0.5s] xl:[animation-fill-mode:backwards]"
					>
						<MoonhubLogo className="h-14 text-black dark:text-white" />
					</a>
					<h1
						data-heading
						className="mt-8 animate-slide-top text-4xl font-medium text-foreground [animation-fill-mode:backwards] [animation-delay:0.3s] md:text-5xl xl:mt-4 xl:animate-slide-left xl:text-6xl xl:[animation-fill-mode:backwards] xl:[animation-delay:0.8s]"
					>
						Fullstack Take-home
					</h1>
					<p
						data-paragraph
						className="mt-6 animate-slide-top text-xl/7 text-muted-foreground [animation-fill-mode:backwards] [animation-delay:0.8s] xl:mt-8 xl:animate-slide-left xl:text-xl/6 xl:leading-10 xl:[animation-fill-mode:backwards] xl:[animation-delay:1s]"
					>
						Log In using the credentials provided for a demo.
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
