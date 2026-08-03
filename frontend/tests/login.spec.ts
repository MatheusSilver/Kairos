import { expect, test } from "@playwright/test"
import { firstApoioCodpes } from "./config.ts"

test.use({ storageState: { cookies: [], origins: [] } })

test("Mock USP users are listed", async ({ page }) => {
  await page.goto("/login")

  await expect(
    page.getByRole("heading", { name: "Entrar com a Senha Única USP" }),
  ).toBeVisible()
  await expect(page.getByTestId(`mock-user-${firstApoioCodpes}`)).toBeVisible()
})

test("Log in as the seeded Apoio user", async ({ page }) => {
  await page.goto("/login")
  await page.getByTestId(`mock-user-${firstApoioCodpes}`).click()

  await page.waitForURL("/")

  await expect(page.getByText("Olá,")).toBeVisible()
})

test("Logged in user is redirected away from login", async ({ page }) => {
  await page.goto("/login")
  await page.getByTestId(`mock-user-${firstApoioCodpes}`).click()
  await page.waitForURL("/")

  await page.goto("/login")
  await page.waitForURL("/")

  expect(page.url()).not.toContain("/login")
})
