import { Metadata } from 'next';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Posteeze - Agent',
  description: '',
};

export default async function Page() {
  return redirect('/agents/new');
}
