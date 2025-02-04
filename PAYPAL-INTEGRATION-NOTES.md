## Using Paypal support from the frontend

Integration Flow
- frontend sends POST to backend to initiate the PayPal payment.
- backend responds with approval_url, which the frontend redirects the user to.
- after the user approves the payment on PayPal, PayPal redirects back to the frontend, and the frontend sends a rewquest to the backend to execute the payment.
- backend finalizes the transaction and stores the payment details in the database.

### Create PayPal Payment

```
import React, { useState } from 'react';

const CreatePayment = () => {
  const [amount, setAmount] = useState(50.00);  // Example amount
  const lenderId = 1;  // Hard-coded for now; replace with actual ID
  const borrowerId = 2;

  const handleCreatePayment = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/create-paypal-payment/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: amount,
          lender_id: lenderId,
          borrower_id: borrowerId,
        }),
      });

      const data = await response.json();
      if (data.approval_url) {
        // Redirect the user to PayPal for payment approval
        window.location.href = data.approval_url;
      } else {
        console.error('Error creating PayPal payment:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Create PayPal Payment</h2>
      <button onClick={handleCreatePayment}>Pay with PayPal</button>
    </div>
  );
};

export default CreatePayment;
```

### Handle PayPal redirect after Payment Approval

When PayPal redirects the user back to your React app after they approve the payment, the URL will contain the payment_id and payer_id parameters.
You'll need to extract these from the URL and send them to the backend to execute the payment.

```
import { useEffect } from 'react';

const ExecutePayment = ({ history }) => {
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const paymentId = urlParams.get('paymentId');
    const payerId = urlParams.get('PayerID');

    if (paymentId && payerId) {
      executePayment(paymentId, payerId);
    }
  }, []);

  const executePayment = async (paymentId, payerId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/execute-paypal-payment/?paymentId=${paymentId}&PayerID=${payerId}`);

      const data = await response.json();
      if (data.message === 'Payment completed successfully') {
        alert('Payment was successful!');
      } else {
        console.error('Error executing payment:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Processing Payment...</h2>
    </div>
  );
};

export default ExecutePayment;

```

### React Routing

To handle PayPal redirects.

```
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CreatePayment from './CreatePayment';
import ExecutePayment from './ExecutePayment';

const App = () => (
  <Router>
    <Switch>
      <Route path="/create-payment" component={CreatePayment} />
      <Route path="/execute-payment" component={ExecutePayment} />
    </Switch>
  </Router>
);

export default App;

```
