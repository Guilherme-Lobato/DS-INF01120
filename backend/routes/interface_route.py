from fastapi import APIRouter, HTTPException, status
from dtos.interface_dto import InterfaceDTO
from controllers.interface_controller import InterfaceController

router = APIRouter()
controller = InterfaceController()


@router.post("/enviar-form")
async def receber_dados(dados: InterfaceDTO):
    try:
        resultado = controller.processar_dados(dados)
        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar a requisição: {str(e)}",
        )
