interface FormError {
  message: string;
  code: string;
}

type FormErrors = Record<string, Array<FormError>>;

interface UserContract {
  id: number | null,
  last_login: string | null,
  username: string | null,
  first_name: string | null,
  last_name: string | null,
  email: string | null,
  is_active: boolean | null,
  date_joined: string | null
}

interface StudentAgentContract {
  id: number | null,
  user: UserContract
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