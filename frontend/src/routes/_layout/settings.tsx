import { createFileRoute } from "@tanstack/react-router"

import { Appearance } from "@/components/Common/Appearance"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/settings")({
  component: UserSettings,
  head: () => ({
    meta: [
      {
        title: "Configurações - Kairos",
      },
    ],
  }),
})

function UserSettings() {
  const { user: currentUser } = useAuth()

  if (!currentUser) {
    return null
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Configurações</h1>
        <p className="text-muted-foreground">
          {currentUser.name} · nº USP {currentUser.codpes}
          {currentUser.is_apoio ? " · Apoio BCC" : ""}
        </p>
      </div>

      <Appearance />
    </div>
  )
}
