from ninja import Schema


class GantStyleConfigContract(Schema):
    background: str
    color: str
    borderRadius: str


class GanttBarConfig(Schema):
    id: str
    hasHandles: bool
    label: str
    style: GantStyleConfigContract


class GanttConfigContract(Schema):
    startGant: str
    stopGant: str
    ganttBarConfig: GanttBarConfig
