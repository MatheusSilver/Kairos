from app.schemas.usp import USPUser, USPVinculo

IME = {
    "siglaUnidade": "IME",
    "nomeUnidade": "Instituto de Matematica e Estatistica",
    "nomeAbreviadoSetor": "MAC",
}

# Development fixtures, used while Senha Unica credentials are not available
MOCK_USERS: list[USPUser] = [
    USPUser(
        loginUsuario="12345678",
        nomeUsuario="Ana Souza Lima",
        tipoUsuario="A",
        emailUspUsuario="ana.lima@usp.br",
        emailPrincipalUsuario="ana.lima@usp.br",
        wsuserid="mock-12345678",
        vinculo=[
            USPVinculo(tipoVinculo="ALUNOGR", nomeVinculo="Aluno de Graduacao", **IME)
        ],
    ),
    USPUser(
        loginUsuario="87654321",
        nomeUsuario="Bruno Martins Alves",
        tipoUsuario="S",
        emailUspUsuario="bruno.alves@usp.br",
        emailPrincipalUsuario="bruno.alves@usp.br",
        wsuserid="mock-87654321",
        vinculo=[
            USPVinculo(
                tipoVinculo="SERVIDOR",
                nomeVinculo="Docente",
                tipoFuncao="Docente",
                **IME,
            )
        ],
    ),
    USPUser(
        loginUsuario="11223344",
        nomeUsuario="Clara Ribeiro Nunes",
        tipoUsuario="A",
        emailUspUsuario="clara.nunes@usp.br",
        emailPrincipalUsuario="clara.nunes@usp.br",
        wsuserid="mock-11223344",
        vinculo=[
            USPVinculo(tipoVinculo="ALUNOGR", nomeVinculo="Aluno de Graduacao", **IME)
        ],
    ),
]


def get_mock_user(login_usuario: str) -> USPUser | None:
    return next((u for u in MOCK_USERS if u.loginUsuario == login_usuario), None)
