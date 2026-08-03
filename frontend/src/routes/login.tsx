import { useQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"

import { AuthService } from "@/client"
import { AuthLayout } from "@/components/Common/AuthLayout"
import { LoadingButton } from "@/components/ui/loading-button"
import useAuth, { isLoggedIn } from "@/hooks/useAuth"

export const Route = createFileRoute("/login")({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Entrar - Kairos",
      },
    ],
  }),
})

function Login() {
  const { loginMutation } = useAuth()

  const { data: uspUsers } = useQuery({
    queryKey: ["mockUsers"],
    queryFn: () => AuthService.listMockUsers(),
  })

  const onSelect = (codpes: string) => {
    if (loginMutation.isPending) return
    loginMutation.mutate(codpes)
  }

  return (
    <AuthLayout>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col items-center gap-2 text-center">
          <h1 className="text-2xl font-bold">Entrar com a Senha Única USP</h1>
          <p className="text-muted-foreground text-sm">
            Ambiente de desenvolvimento — escolha um usuário simulado
          </p>
        </div>

        <div className="grid gap-3">
          {uspUsers?.map((uspUser) => (
            <LoadingButton
              key={uspUser.loginUsuario}
              data-testid={`mock-user-${uspUser.loginUsuario}`}
              variant="outline"
              loading={loginMutation.isPending}
              onClick={() => onSelect(uspUser.loginUsuario)}
              className="h-auto flex-col items-start gap-1 py-3"
            >
              <span className="font-medium">{uspUser.nomeUsuario}</span>
              <span className="text-muted-foreground text-xs">
                {uspUser.loginUsuario} ·{" "}
                {uspUser.vinculo?.[0]?.nomeVinculo ?? "Sem vínculo"}
              </span>
            </LoadingButton>
          ))}
        </div>
      </div>
    </AuthLayout>
  )
}
