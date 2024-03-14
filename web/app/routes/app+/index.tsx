import { type MetaFunction } from '@remix-run/node'

export const meta: MetaFunction = () => [{ title: 'Dashboard | Moonhub Takehome' }]

export default function MainApp() {
    return (
        <div>
            <div>
                <div>
                    <h1>Welcome to the dashboard!</h1>
                </div>
            </div>
        </div>
    )
}