import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default memo(({ data, selected, isConnectable }) => {
    return (
        <>
            <Handle
                type="target"
                position={Position.Top}
                style={{ background: '#555' }}
                onConnect={(params) => console.log('handle onConnect', params)}
                isConnectable={isConnectable}
            />
            <Card sx={{ border: selected ? '2px solid #1976d2' : 'none' }}>
                <CardContent>
                    <Typography variant="h6">
                        {data.name}
                    </Typography>
                    <Typography variant="body2">
                        {data.description}
                    </Typography>
                </CardContent>
            </Card>
            <Handle
                type="source"
                position={Position.Bottom}
                style={{ background: '#555' }}
                onConnect={(params) => console.log('handle onConnect', params)}
                isConnectable={isConnectable}
            />
        </>
    );
});
