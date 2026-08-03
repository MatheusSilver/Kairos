from sqlmodel import Field, SQLModel


# Field names mirror the Senha Unica USP payload
class USPVinculo(SQLModel):
    tipoVinculo: str
    nomeVinculo: str | None = None
    tipoFuncao: str | None = None
    siglaUnidade: str | None = None
    nomeUnidade: str | None = None
    nomeAbreviadoSetor: str | None = None


class USPUser(SQLModel):
    loginUsuario: str
    nomeUsuario: str
    tipoUsuario: str | None = None
    emailPrincipalUsuario: str | None = None
    emailAlternativoUsuario: str | None = None
    emailUspUsuario: str | None = None
    wsuserid: str | None = None
    vinculo: list[USPVinculo] = Field(default_factory=list)
