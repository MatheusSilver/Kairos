import { test as setup } from "@playwright/test"
import { firstApoioCodpes } from "./config.ts"

const authFile = "playwright/.auth/user.json"

setup("authenticate", async ({ page }) => {
  await page.goto("/login")
  await page.getByTestId(`mock-user-${firstApoioCodpes}`).click()
  await page.waitForURL("/")
  await page.context().storageState({ path: authFile })
})
