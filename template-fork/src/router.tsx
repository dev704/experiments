import { createRootRoute, createRoute, Outlet } from '@tanstack/react-router'
import { Flex, Heading, Text } from '@radix-ui/themes'

const rootRoute = createRootRoute({
  component: () => <Outlet />,
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => (
    <Flex direction="column" align="center" justify="center" style={{ minHeight: '100vh' }} gap="3">
      <Heading size="6">template-react-site</Heading>
      <Text color="gray">Your app starts here.</Text>
    </Flex>
  ),
})

export const routeTree = rootRoute.addChildren([indexRoute])
