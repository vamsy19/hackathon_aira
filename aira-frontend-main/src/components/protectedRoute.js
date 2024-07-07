import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const isLoggedIn = () => {
    return !!localStorage.getItem('accessToken');
};


const ProtectedRoute = ({ component: Component, ...rest }) => (
    <Route
        {...rest}
        render={props =>
            isLoggedIn() ? (
                <Component {...props} />
            ) : (
                <Navigate to="/login" />
            )
        }
    />
);

export default ProtectedRoute;