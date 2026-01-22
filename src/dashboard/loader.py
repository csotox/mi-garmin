import json
from pathlib import Path

from src.dashboard.models import DashboardDataV1


#-- - Me gustan los metodos encadenados, vamos como se pueden implementar
class DashboardLoader:
    def __init__(self, path: str = "data/outputs/kpi_week.json") -> None:
        self.path = Path(path)
        self.json: dict = {}

    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"No existe archivo dashboard: {self.path}")

        self.json = json.loads(self.path.read_text(encoding="utf-8"))

        #-- - Necesito esta protección porque el schema del archivo json va a evolucionar
        #-- - No quiero romper funcionalidad cuando este implementando una nueva versión
        #-- - [TODO] Tal vez deberia recibir la versión del eschema como parámetro
        #-- - no me decido todavía, espero a ver como avanzo y si tiene sentido.
        #-- - NOTA: También puede ser una config en .env
        #-- - [TODO] Por separación de responsabilidades, esta validación debería ser
        #-- - un metodo por ahora para mantener simple los metodos encadenados dejo
        #-- - la validación aquí.
        version = self.json.get("schema_version")
        if version != "v1":
            raise ValueError(f"Schema no soportado: {version}")

        return self

    def parse(self) -> DashboardDataV1:
        return DashboardDataV1(**self.json)
