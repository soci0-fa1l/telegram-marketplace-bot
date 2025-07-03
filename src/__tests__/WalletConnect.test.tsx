import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import WalletConnect from '../components/WalletConnect';

test('renders connect button', () => {
  render(<WalletConnect />);
  expect(screen.getByRole('button', { name: '지갑 연결' })).toBeInTheDocument();
});
