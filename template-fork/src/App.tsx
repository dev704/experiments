import { RouterProvider, createRouter } from '@tanstack/react-router'
import { Theme } from '@radix-ui/themes'
import '@radix-ui/themes/styles.css'
import { routeTree } from './router'

const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

function App() {
  return (
    <Theme>
      <RouterProvider router={router} />
    </Theme>
  )
}

export default App
