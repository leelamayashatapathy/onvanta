import { Link } from "react-router-dom";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";

export function ForgotPasswordPage() {
  return (
    <Card className="p-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold text-slate-900">Reset password</h2>
        <p className="text-sm text-slate-600">
          Placeholder — password reset flow will be wired to the backend in Phase 2.
        </p>
      </div>

      <div className="mt-6 space-y-3">
        <Button variant="secondary" className="w-full" disabled>
          Send reset link
        </Button>
        <Link className="block text-center text-sm font-medium text-blue-600" to="/login">
          Back to sign in
        </Link>
      </div>
    </Card>
  );
}
