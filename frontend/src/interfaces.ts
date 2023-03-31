interface FormError {
  message: string;
  code: string;
}

type FormErrors = Record<string, Array<FormError>>;

interface UserContract {
  id?: number | null,
  username: string | null,
  first_name: string | null,
  last_name: string | null,
  email: string | null,
  is_active: boolean | null,
}

interface StudentAgentContract {
  id?: number | null,
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


interface LocationContract {
  uuid?: string | null,
  label: string,
  description: string | null,
  content?: string | null,
  address1: string,
  address2: string | null,
  city: string,
  country: string,
  cover?: {
    path: string,
    url: string
  }
}

interface LocationListResponse {
  count: number,
  model: string,
  items: Array<LocationContract>
}

interface LocationSingleResponse {
  count: number,
  model: string,
  item: LocationContract
}

export {
  FormError,
  FormErrors,
  StudentAgentContract,
  StudentListResponse,
  StudentSingleResponse,
  LocationContract,
  LocationListResponse,
  LocationSingleResponse
}