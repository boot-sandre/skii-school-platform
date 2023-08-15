interface FormError {
  message: string;
  code: string;
}

type FormErrors = Record<string, Array<FormError>>;

interface StudentAgentContract {
  id: number,
  user_id: number
}

interface StudentListResponse {
  count: number,
  model: string,
  items: Array<StudentAgentContract>
}

interface StudentSingleResponse {
  count: number,
  model: string,
  item: StudentAgentContract
}

export {
  FormError,
  FormErrors,
  StudentAgentContract,
  StudentListResponse,
  StudentSingleResponse,
}