export interface Gym {
    id: number
    name: string
    address: string
    city: string
    state: string
    post_code: string
    latitude: number
    longitude: number
    created_at: string
    is_active: boolean
}

export interface Trainer {
    id: number
    email: string
    first_name: string
    last_name: string
    bio?: string
    specializations?: string
    certifications?: string
    hourly_rate?: number
    years_experience?: number
    created_at: string
    is_active: boolean
    is_available: boolean
}