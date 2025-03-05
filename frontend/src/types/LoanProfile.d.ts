export default interface LoanProfile {
  id: number;
  title: string;
  description: string;
  profile_img: string;
  country: string;
  city: string;
  deadline_to_receive_loan: string;
  loan_duration: number;
  target_amount: string;
  total_raised: string;
  total_repaid: string;
  remaining_balance: string;
}

