import { type MetaFunction } from '@remix-run/node'

export const meta: MetaFunction = () => [{ title: 'Projects | Moonhub Takehome' }]

export default function ProjectsIndex() {
    return (
        <div>
            <div>
                <div>
                    <h1>Projects home!</h1>
                </div>
            </div>
        </div>
    )
}