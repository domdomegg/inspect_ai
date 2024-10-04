from inspect_ai._util.registry import registry_log_name
from inspect_ai.solver._task_state import TaskState
from inspect_ai.tool._tool_call import ToolCall

from ._approval import Approval
from ._approver import Approver, ApproverToolView


async def call_approver(
    approver: Approver,
    tool_call: ToolCall,
    tool_view: ApproverToolView | None = None,
    state: TaskState | None = None,
) -> Approval:
    # run approver
    approval = await approver(tool_call, tool_view, state)

    # record
    record_approval(registry_log_name(approver), tool_call, approval, tool_view)

    # return approval
    return approval


def record_approval(
    approver_name: str,
    tool_call: ToolCall,
    approval: Approval,
    tool_view: ApproverToolView | None,
) -> None:
    from inspect_ai.log._transcript import ApprovalEvent, transcript

    transcript()._event(
        ApprovalEvent(
            tool_call=tool_call,
            tool_view=tool_view,
            approver=approver_name,
            decision=approval.decision,
            explanation=approval.explanation,
        )
    )
