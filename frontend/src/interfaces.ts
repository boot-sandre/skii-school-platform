interface FormError {
  message: string;
  code: string;
}

type FormErrors = Record<string, Array<FormError>>;

interface StudentAgentContract {
  id: number,
  user_id: number
}

export {
  FormError,
  FormErrors,
  StudentAgentContract
}